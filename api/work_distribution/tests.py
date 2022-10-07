import random

from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
    override_settings,
)

from .exceptions import UsersCountLessThenFour, WorkDistributionAlreadyExists
from .models import WorkDistributionToEvaluate
from ..control.models import WeekID
from ..models import User
from ..rus.models import Essay, Text


class WorkDistributionTest(APITestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def setUp(self) -> None:
        call_command('init_stage')
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.admin_user = User.objects.create_superuser(username='admin_user')
        self.assign_text(self.admin_user)
        self.switch_stage()

    def assign_text(self, teacher_user):
        data = {
            "body": "jkjhgkjtytyhdtykuil",
            "author": "u77",
            "author_description": "g2yn8g2y3g923",
            "teacher": teacher_user.id,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

    def switch_stage(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S2')
        self.client.credentials()

    def test_no_users(self):
        self.assertRaises(
            UsersCountLessThenFour,
            WorkDistributionToEvaluate.make_necessary_for_week_participants,
        )

    def create_common_user_and_send_essay(self, username: str):

        user = User.objects.create_user(username)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        Essay.objects.create(
            task=Text.get_current(),
            body="vrhnuivwq9ov3vn 8" + user.username,
            author=user,
        )

    def test_1_essay(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.assertRaises(
            UsersCountLessThenFour,
            WorkDistributionToEvaluate.make_necessary_for_week_participants,
        )

    def test_2_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.assertRaises(
            UsersCountLessThenFour,
            WorkDistributionToEvaluate.make_necessary_for_week_participants,
        )

    def test_3_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.create_common_user_and_send_essay('common_user_3')
        self.assertRaises(
            UsersCountLessThenFour,
            WorkDistributionToEvaluate.make_necessary_for_week_participants,
        )

    def test_4_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.create_common_user_and_send_essay('common_user_3')
        self.create_common_user_and_send_essay('common_user_4')

        WorkDistributionToEvaluate.make_necessary_for_week_participants()

        self.assertEqual(
            WorkDistributionToEvaluate.objects.all().count(), 3 * 4
        )  # по 3 назначения для 4 пользователей

    def test_5_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.create_common_user_and_send_essay('common_user_3')
        self.create_common_user_and_send_essay('common_user_4')
        self.create_common_user_and_send_essay('common_user_5')

        WorkDistributionToEvaluate.make_necessary_for_week_participants()

        self.assertEqual(
            WorkDistributionToEvaluate.objects.all().count(), 4 * 5
        )  # по 4 назначения для 5 пользователей

    def make_N_essay_distribution(self, n: int, clear_after: bool = True):
        participants_count = n
        for i in range(4, participants_count + 4):
            self.create_common_user_and_send_essay(f'common_user_{i}')
        self.assertEqual(Essay.objects.all().count(), participants_count)
        WorkDistributionToEvaluate.make_necessary_for_week_participants()
        self.assertEqual(
            WorkDistributionToEvaluate.objects.all().count(),
            (participants_count - 1) * participants_count,
        )  # по (participants_count - 1) назначения для participants_count пользователей
        if clear_after:
            Essay.objects.all().delete()
            User.objects.filter(username__startswith='common_user_').delete()

    def test_10_essays(self):
        self.make_N_essay_distribution(10)

    def test_random_essays(self):
        for i in range(6, 50, 5):
            self.make_N_essay_distribution(i)
        self.make_N_essay_distribution(100)

    def test_1_volunteer(self):
        participants_count = 12
        for i in range(4, participants_count + 4):
            self.create_common_user_and_send_essay(f'common_user_{i}')

        WorkDistributionToEvaluate.make_optionally_for_volunteer(self.admin_user)
        self.assertEqual(
            WorkDistributionToEvaluate.objects.all().count(), participants_count
        )

    def test_1_volunteer_with_eq_rating(self):
        participants_count = 12
        for i in range(4, participants_count + 4):
            self.create_common_user_and_send_essay(f'common_user_{i}')

        common_user_4 = User.objects.get(username='common_user_4')
        common_user_4.rating = 100
        common_user_4.save()
        self.admin_user.rating = 100
        self.admin_user.save()

        WorkDistributionToEvaluate.make_optionally_for_volunteer(self.admin_user)
        first_work_to_evaluate = WorkDistributionToEvaluate.objects.filter(
            evaluator=self.admin_user
        ).first()
        self.assertEqual(first_work_to_evaluate.work.author, common_user_4)
        for future_eval in WorkDistributionToEvaluate.objects.filter(
            evaluator=self.admin_user
        ):
            self.assertEqual(future_eval.is_required, False)

    def test_10_distributions_is_required(self):
        self.make_N_essay_distribution(10, clear_after=False)

        picked_user = User.objects.get(username='common_user_7')

        i = 0
        for future_eval in WorkDistributionToEvaluate.objects.filter(
            evaluator=picked_user, week_id=WeekID.get_current()
        ):
            if i in [0, 1, 2]:
                self.assertEqual(future_eval.is_required, True)
            else:
                self.assertEqual(future_eval.is_required, False)
            i += 1

        self.assertEqual(
            WorkDistributionToEvaluate.objects.filter(
                week_id=WeekID.get_current(), is_required=True
            ).count(),
            3 * 10,
        )

    def test_distribution_no_ourself_user(self):
        self.make_N_essay_distribution(25, clear_after=False)

        for participant in User.objects.filter(username__startswith='common_user_'):
            for future_eval in WorkDistributionToEvaluate.objects.filter(
                week_id=WeekID.get_current(), evaluator=participant
            ):
                self.assertNotEqual(future_eval.work.author, participant)

    def test_distribution_set_user_ratings(self):
        participants_count = 15
        for i in range(1, participants_count + 1):
            self.create_common_user_and_send_essay(f'iuweqng_user_{i}')

        for participant in User.objects.filter(username__startswith='iuweqng_user_'):
            participant.rating = random.randint(10, 300)
            participant.save()
        WorkDistributionToEvaluate.make_necessary_for_week_participants()
        self.assertEqual(
            WorkDistributionToEvaluate.objects.all().count(),
            (participants_count - 1) * participants_count,
        )
        self.assertEqual(
            WorkDistributionToEvaluate.objects.filter(
                week_id=WeekID.get_current(), is_required=True
            ).count(),
            3 * participants_count,
        )
        for participant in User.objects.filter(username__startswith='iuweqng_user_'):
            i = 0
            for future_eval in WorkDistributionToEvaluate.objects.filter(
                evaluator=participant, week_id=WeekID.get_current()
            ):
                if i in [0, 1, 2]:
                    self.assertEqual(future_eval.is_required, True)
                else:
                    self.assertEqual(future_eval.is_required, False)
                i += 1

        for participant in User.objects.filter(username__startswith='iuweqng_user_'):
            for future_eval in WorkDistributionToEvaluate.objects.filter(
                week_id=WeekID.get_current(), evaluator=participant
            ):
                self.assertNotEqual(future_eval.work.author, participant)

    def test_double_distribution(self):
        self.make_N_essay_distribution(10, clear_after=False)
        self.assertRaises(
            WorkDistributionAlreadyExists,
            WorkDistributionToEvaluate.make_necessary_for_week_participants,
        )
