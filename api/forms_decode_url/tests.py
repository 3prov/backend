from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
    override_settings,
)

from api.form_url.models import EvaluationFormURL
from api.models import User
from api.rus.evaluations.models import EssayEvaluation, EssaySelectionReview


class ControlTest(APITestCase):
    def setUp(self) -> None:
        call_command('init_stage')
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin_user')
        self.common_user = User.objects.create_user(username='common_user')

    def assign_text(self, user_to_return: User):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.admin_user.id,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        self.client.post(reverse('text_assign'), data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_to_return.auth_token}')

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

    def test_simulate_essay_pass(self):
        self.assign_text(self.common_user)
        self.switch_stage(self.common_user)
        encoded_url = self.get_link_to_essay_form(self.common_user)
        response = self.client.get(
            reverse('form_essay_by_encoded_part', args=[encoded_url])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['essay_already_sent'], False)
        self.assertIsNone(response.json()['essay'])
        data = {'body': 'тест.'}
        response = self.client.post(
            reverse('essay_from_url_post', args=[encoded_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            reverse('form_essay_by_encoded_part', args=[encoded_url])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['essay_already_sent'], True)
        self.assertEqual(response.json()['essay']['body'], data['body'])

        data = {'body': 'теперь измененное содержимое!'}
        response = self.client.patch(
            reverse('essay_from_url_edit', args=[encoded_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('form_essay_by_encoded_part', args=[encoded_url])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['essay_already_sent'], True)
        self.assertEqual(response.json()['essay']['body'], data['body'])

    def send_essay_from_user(self, user: User):
        encoded_url = self.get_link_to_essay_form(user)
        response = self.client.get(
            reverse('form_essay_by_encoded_part', args=[encoded_url])
        )
        data = {'body': f'сочинение от {user.username}.'}
        response = self.client.post(
            reverse('essay_from_url_post', args=[encoded_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_simulate_evaluation_pass(self):
        self.assign_text(self.common_user)
        self.switch_stage(self.common_user)
        common_user2 = User.objects.create_user(username='common_user2')
        self.send_essay_from_user(common_user2)
        common_user3 = User.objects.create_user(username='common_user3')
        self.send_essay_from_user(common_user3)
        common_user4 = User.objects.create_user(username='common_user4')
        self.send_essay_from_user(common_user4)
        common_user5 = User.objects.create_user(username='common_user5')
        self.send_essay_from_user(common_user5)

        self.switch_stage(self.common_user)
        self.assertEqual(EvaluationFormURL.objects.all().count(), 3 * 4)

        form_eval = EvaluationFormURL.objects.first()
        response = self.client.get(
            reverse('form_evaluation_by_encoded_part', args=[form_eval.url])
        )
        self.assertIsNotNone(response.json()['essay']['body'])
        self.assertEqual(response.json()['evaluation_already_sent'], False)
        self.assertIsNone(response.json()['evaluation'])

        data = {
            "criteria": {
                "k1": 0,
                "k2": 1,
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
        self.assertEqual(EssayEvaluation.objects.all().count(), 0)
        response = self.client.post(
            reverse('evaluation_from_url_post', args=[form_eval.url]),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EssayEvaluation.objects.all().count(), 1)
        id_before_change = response.json()['criteria']['id']
        for i in range(1, 13):
            self.assertEqual(
                response.json()['criteria'][f'k{i}'], data['criteria'][f'k{i}']
            )

        response = self.client.post(
            reverse('evaluation_from_url_post', args=[form_eval.url]),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EssayEvaluation.objects.all().count(), 1)

        response = self.client.post(
            reverse('evaluation_from_url_post', args=[form_eval.url]),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            reverse('form_evaluation_by_encoded_part', args=[form_eval.url])
        )
        self.assertIsNotNone(response.json()['essay']['body'])
        self.assertEqual(response.json()['evaluation_already_sent'], True)
        self.assertIsInstance(response.json()['evaluation'], dict)
        data = {
            "criteria": {
                "k1": 1,
                "k2": 0,
                "k3": 0,
                "k4": 0,
                "k5": 0,
                "k6": 0,
                "k7": 0,
                "k8": 0,
                "k9": 0,
                "k10": 0,
                "k11": 0,
                "k12": 0,
            }
        }
        response = self.client.patch(
            reverse('evaluation_from_url_edit', args=[form_eval.url]),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EssayEvaluation.objects.all().count(), 1)
        response = self.client.get(
            reverse('evaluation_from_url_edit', args=[form_eval.url]), format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EssayEvaluation.objects.all().count(), 1)
        for i in range(1, 13):
            self.assertEqual(
                response.json()['criteria'][f'k{i}'], data['criteria'][f'k{i}']
            )
        self.assertEqual(id_before_change, response.json()['criteria']['id'])
        data['criteria']['k3'] = 10
        response = self.client.patch(
            reverse('evaluation_from_url_edit', args=[form_eval.url]),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, 400)

        data = {
            "start_selection_char_index": 5,
            "selection_length": 15,
            "evaluator_comment": "Мой комментарий, длина которого 15!!!!",
            "mistake_type": "K09",
        }
        self.assertEqual(EssaySelectionReview.objects.all().count(), 0)
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()['evaluator_comment'], data['evaluator_comment']
        )
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 1)
        data['mistake_type'] = 'K11'
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 1)

        data['evaluator_comment'] = 'комментарий к фрагменту (изменённый).'
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['detail'], 'Проверка этого фрагмента уже отправлена.'
        )
        self.assertEqual(EssaySelectionReview.objects.all().count(), 1)

        data['start_selection_char_index'] = 2
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['start_selection_char_index'] = 0
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['start_selection_char_index'] = -1
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['start_selection_char_index'] = 26
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 3)

        data['start_selection_char_index'] = 24
        data['selection_length'] = 1
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 4)

        data['start_selection_char_index'] = 24
        data['selection_length'] = 2
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 5)

        data['start_selection_char_index'] = 24
        data['selection_length'] = 3
        response = self.client.post(
            reverse(
                'evaluation_essay_selection_review_form_url_post', args=[form_eval.url]
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 5)

        data['evaluator_comment'] = 'изменённый'
        response = self.client.put(
            reverse(
                'evaluation_essay_selection_review_form_url_edit',
                kwargs={
                    'encoded_part': form_eval.url,
                    'start_selection_char_index': 24,
                    'selection_length': 3,
                },
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(
            reverse(
                'evaluation_essay_selection_review_form_url_edit',
                kwargs={
                    'encoded_part': form_eval.url,
                    'start_selection_char_index': 24,
                    'selection_length': 2,
                },
            ),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(EssaySelectionReview.objects.all().count(), 5)
        self.assertEqual(
            response.json()['evaluator_comment'], data['evaluator_comment']
        )
