from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from .exceptions import UsersCountLessThenFour, WorkDistributionAlreadyExists
from .models import WorkDistributionToEvaluate
from ..management import init_stage
from ..models import User
from ..rus.models import Essay


class WorkDistributionTest(APITestCase):

    def setUp(self) -> None:
        init_stage()
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
            "teacher": teacher_user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}')
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

    def switch_stage(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S2')
        self.client.credentials()

    def test_no_users(self):
        self.assertRaises(UsersCountLessThenFour, WorkDistributionToEvaluate.make_necessary_for_week_participants)

    def create_common_user_and_send_essay(self, username: str):

        user = User.objects.create_user(username)
        data = {
            "body": "vrhnuivwq9ov3vn 8 9 234n834f7834v83vyo3n4i8348ov3y4vgony8giv o34viuo4qvi" + user.username,
            "author": user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        response = self.client.post(reverse('essay_pass'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_1_essay(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.assertRaises(UsersCountLessThenFour, WorkDistributionToEvaluate.make_necessary_for_week_participants)

    def test_2_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.assertRaises(UsersCountLessThenFour, WorkDistributionToEvaluate.make_necessary_for_week_participants)

    def test_3_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.create_common_user_and_send_essay('common_user_3')
        self.assertRaises(UsersCountLessThenFour, WorkDistributionToEvaluate.make_necessary_for_week_participants)

    def test_4_essays(self):
        self.create_common_user_and_send_essay('common_user_1')
        self.create_common_user_and_send_essay('common_user_2')
        self.create_common_user_and_send_essay('common_user_3')
        self.create_common_user_and_send_essay('common_user_4')

        WorkDistributionToEvaluate.make_necessary_for_week_participants()

        self.assertEqual(WorkDistributionToEvaluate.objects.all().count(), 3 * 4)  # по 3 назначения для 4 пользователей


