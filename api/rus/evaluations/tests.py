from random import randint
from uuid import UUID

from django.core.management import call_command

from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
    override_settings,
)
from rest_framework import status
from rest_framework.reverse import reverse

from api.form_url.models import EvaluationFormURL
from api.models import User
from api.rus.evaluations.models import EssayEvaluation
from api.rus.models import Text, Essay
from api.services import all_objects, filter_objects, get_object


class EvaluationsTest(APITestCase):
    def setUp(self) -> None:
        call_command('init_stage')
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.create_users_with_ratings()
        self.admin_user = User.objects.create_superuser(username='test_admin')
        self.assign_text()

    @staticmethod
    def get_teacher_uuid() -> str:
        return User.objects.create_superuser(username='test_admin_teacher').id

    @staticmethod
    def create_one_user_with_random_rating(username: str) -> User:
        return User.objects.create_user(username=username, rating=randint(50, 500))

    def create_users_with_ratings(self):
        self.common_user_1 = self.create_one_user_with_random_rating('common_user_1')
        self.common_user_2 = self.create_one_user_with_random_rating('common_user_2')
        self.common_user_3 = self.create_one_user_with_random_rating('common_user_3')
        self.common_user_4 = self.create_one_user_with_random_rating('common_user_4')
        self.common_user_5 = self.create_one_user_with_random_rating('common_user_5')
        self.volunteer_1 = self.create_one_user_with_random_rating('volunteer_1')
        self.volunteer_2 = self.create_one_user_with_random_rating('volunteer_2')

    def assign_text(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid(),
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(all_objects(Text.objects).count(), 1)

    def switch_stage(self, user_to_return):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        self.client.get(reverse('switch_stage_to_next'))
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_to_return.auth_token}')

    def get_link_to_essay_form(self, user: User) -> str:
        data = {'user': user.id}
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()['url']

    def send_essay_from_user(self, user: User):
        encoded_url = self.get_link_to_essay_form(user)
        data = {'body': f'сочинение от {user.username}.'}
        response = self.client.post(
            reverse('essay_from_url_post', args=[encoded_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def send_evaluation_from_user_with_form_url(self, user: User, form_url_url: str):
        data = {
            "criteria": {
                "k1": randint(0, 1),
                "k2": randint(0, 6),
                "k3": 1,
                "k4": 0,
                "k5": 0,
                "k6": 0,
                "k7": 1,
                "k8": 0,
                "k9": 0,
                "k10": 1,
                "k11": 0,
                "k12": 1,
            }
        }
        response = self.client.post(
            reverse('evaluation_from_url_post', args=[form_url_url]),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def send_all_required_evaluations_from_user(self, user: User):
        form_eval = filter_objects(EvaluationFormURL.objects, user=user)
        for evaluation in form_eval:
            self.send_evaluation_from_user_with_form_url(
                evaluation.user, evaluation.url
            )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_evaluate_from_participant_is_volunteer_5(self):
        def _check_one(user: User):
            response = self.client.get(
                reverse('volunteer_get_distribution', args=[user.id])
            )
            self.assertEqual(
                response.json()['count'], all_objects(Essay.objects).count() - 1
            )
            self.assertEqual(
                len(response.json()['results']), all_objects(Essay.objects).count() - 1
            )
            response = self.client.get(
                reverse('volunteer_get_distribution', args=[user.id])
            )
            self.assertEqual(
                response.json()['count'], all_objects(Essay.objects).count() - 1
            )
            self.assertEqual(
                len(response.json()['results']), all_objects(Essay.objects).count() - 1
            )

            set_of_work_authors = set()
            for evaluation in response.json()['results']:
                self.assertEqual(UUID(evaluation['evaluator']), user.id)
                self.assertNotEqual(
                    get_object(Essay.objects, id=UUID(evaluation['work'])).author, user
                )
                set_of_work_authors.add(
                    get_object(Essay.objects, id=UUID(evaluation['work'])).author
                )
            self.assertEqual(
                len(set_of_work_authors), all_objects(Essay.objects).count() - 1
            )

        self.switch_stage(self.admin_user)
        self.send_essay_from_user(self.common_user_1)
        self.send_essay_from_user(self.common_user_2)
        self.send_essay_from_user(self.common_user_3)
        self.send_essay_from_user(self.common_user_4)
        self.send_essay_from_user(self.common_user_5)
        self.switch_stage(self.admin_user)
        self.send_all_required_evaluations_from_user(self.common_user_1)
        self.send_all_required_evaluations_from_user(self.common_user_2)
        self.send_all_required_evaluations_from_user(self.common_user_3)
        self.send_all_required_evaluations_from_user(self.common_user_4)
        self.send_all_required_evaluations_from_user(self.common_user_5)

        _check_one(self.common_user_2)
        _check_one(self.common_user_3)
        _check_one(self.common_user_1)
        _check_one(self.common_user_5)
        _check_one(self.common_user_4)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_evaluate_from_participant_4(self):
        self.switch_stage(self.admin_user)
        self.send_essay_from_user(self.common_user_1)
        self.send_essay_from_user(self.common_user_2)
        self.send_essay_from_user(self.common_user_3)
        self.send_essay_from_user(self.common_user_4)
        self.switch_stage(self.admin_user)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 0)
        self.send_all_required_evaluations_from_user(self.common_user_1)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 3)
        self.send_all_required_evaluations_from_user(self.common_user_2)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 6)
        self.send_all_required_evaluations_from_user(self.common_user_3)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 9)
        self.send_all_required_evaluations_from_user(self.common_user_4)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 12)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_evaluate_from_participant_5(self):
        self.switch_stage(self.admin_user)
        self.send_essay_from_user(self.common_user_1)
        self.send_essay_from_user(self.common_user_2)
        self.send_essay_from_user(self.common_user_3)
        self.send_essay_from_user(self.common_user_4)
        self.send_essay_from_user(self.common_user_5)
        self.switch_stage(self.admin_user)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 0)
        self.send_all_required_evaluations_from_user(self.common_user_1)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 3)
        self.send_all_required_evaluations_from_user(self.common_user_2)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 6)
        self.send_all_required_evaluations_from_user(self.common_user_3)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 9)
        self.send_all_required_evaluations_from_user(self.common_user_4)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 12)
        self.send_all_required_evaluations_from_user(self.common_user_5)
        self.assertEqual(all_objects(EssayEvaluation.objects).count(), 15)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def evaluate_from_volunteer_n(self, users: set[User]):
        self.switch_stage(self.admin_user)
        for user in users:
            self.send_essay_from_user(user)
        self.switch_stage(self.admin_user)
        for user in users:
            self.send_all_required_evaluations_from_user(user)

        response = self.client.get(
            reverse('volunteer_get_distribution', args=[self.volunteer_1.id])
        )
        self.assertEqual(response.json()['count'], all_objects(Essay.objects).count())
        self.assertEqual(
            len(response.json()['results']), all_objects(Essay.objects).count()
        )
        response = self.client.get(
            reverse('volunteer_get_distribution', args=[self.volunteer_1.id])
        )
        self.assertEqual(response.json()['count'], all_objects(Essay.objects).count())
        self.assertEqual(
            len(response.json()['results']), all_objects(Essay.objects).count()
        )

        for i in range(1, all_objects(Essay.objects).count() + 1):
            response = self.client.post(
                reverse(
                    'volunteer_create_next_and_get_form_urls_user',
                    args=[self.volunteer_1.id],
                )
            )
            self.assertEqual(len(response.json()), i)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for i in range(2):
            response = self.client.post(
                reverse(
                    'volunteer_create_next_and_get_form_urls_user',
                    args=[self.volunteer_1.id],
                )
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json()), all_objects(Essay.objects).count())

        response = self.client.post(
            reverse(
                'volunteer_create_next_and_get_form_urls_user',
                args=[self.volunteer_1.id],
            )
        )
        for i in range(all_objects(Essay.objects).count()):
            self.send_evaluation_from_user_with_form_url(
                self.volunteer_1, response.json()[i]['url']
            )

    def test_evaluate_from_volunteer_5(self):
        users = {
            self.common_user_1,
            self.common_user_2,
            self.common_user_3,
            self.common_user_4,
            self.common_user_5,
        }
        self.evaluate_from_volunteer_n(users)

    def test_evaluate_from_volunteer_6(self):
        users = {
            self.common_user_1,
            self.common_user_2,
            self.common_user_3,
            self.common_user_4,
            self.common_user_5,
            self.create_one_user_with_random_rating('common_user_6'),
        }
        self.evaluate_from_volunteer_n(users)

    def test_evaluate_from_volunteer_7(self):
        users = {
            self.common_user_1,
            self.common_user_2,
            self.common_user_3,
            self.common_user_4,
            self.common_user_5,
            self.create_one_user_with_random_rating('common_user_6'),
            self.create_one_user_with_random_rating('common_user_7'),
        }
        self.evaluate_from_volunteer_n(users)
