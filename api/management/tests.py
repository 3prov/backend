from datetime import datetime
import freezegun

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from . import init_stage
from .utils import ManagementUtils
from ..models import User


class ManagementTest(APITestCase):
    def setUp(self) -> None:
        init_stage()
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_anon_user_get_state(self):
        response = self.client.get(reverse('get_stage'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_get_state(self):
        common_user = User.objects.create_user(username='common_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {common_user.auth_token}')
        response = self.client.get(reverse('get_stage'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_get_state(self):
        admin_user = User.objects.create_superuser(username='test_admin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        response = self.client.get(reverse('get_stage'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anon_user_switch_stage_to_next(self):
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_switch_stage_to_next(self):
        common_user = User.objects.create_user(username='common_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {common_user.auth_token}')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_switch_stage_to_next(self):
        admin_user = User.objects.create_superuser(username='test_admin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_switch_stage_to_next_looped(self):
        admin_user = User.objects.create_superuser(username='test_admin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S2')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S3')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S4')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S1')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S2')

    def test_admin_user_switch_stage_to_next_many_times(self):
        admin_user = User.objects.create_superuser(username='test_admin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        responses_set = set()
        response = self.client.get(reverse('switch_stage_to_next'))
        prev = response.json()['current_stage']
        for i in range(1, 30):
            response = self.client.get(reverse('switch_stage_to_next'))
            _key_stage = response.json()['current_stage']
            responses_set.add(_key_stage)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(_key_stage, prev)
            prev = _key_stage
        self.assertEqual(len(responses_set), 4)

    def test_anon_user_statistics(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_statistics(self):
        common_user = User.objects.create_user(username='common_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {common_user.auth_token}')
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_statistics(self):
        admin_user = User.objects.create_superuser(username='admin_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['rus']['essays_passed'], 0)

    def assign_text(self, teacher_user):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": teacher_user.id,
        }

        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def switch_stage(self):
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(response.json()['current_stage'], 'S2')

    def pass_essay(self, admin_user):
        data = {
            "body": "vrhnuivwq9ov3vn 8 9 234n834f7834v83vyo3n4i8348ov3y4vgony8giv o34viuo4qvi",
            "author": admin_user.id,
        }
        response = self.client.post(reverse('essay_pass'), data, format='json')

    def test_admin_user_statistics_with_essays(self):
        admin_user = User.objects.create_superuser(username='admin_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        self.assign_text(admin_user)
        self.switch_stage()
        self.pass_essay(admin_user)
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['rus']['essays_passed'], 1)

        self.pass_essay(admin_user)
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['rus']['essays_passed'], 1)

    @freezegun.freeze_time('2022-08-15 01:00')
    def test_get_current_time(self):
        self.assertEqual(
            ManagementUtils.get_current_time(),
            datetime.fromisoformat('2022-08-15 01:00'),
        )

    def get_current_stage_end_time_set_time(self, frozen_time: str, needed_time: str):
        with freezegun.freeze_time(frozen_time):
            response = self.client.get(reverse('get_current_stage_end_time'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                datetime.fromisoformat(response.json()['time']['server_current']),
                datetime.fromisoformat(frozen_time),
            )
            self.assertEqual(
                datetime.fromisoformat(response.json()['time']['stage_end']),
                datetime.fromisoformat(needed_time),
            )

    def test_get_current_stage_end_time(self):
        self.get_current_stage_end_time_set_time('2022-08-15 00:01', '2022-08-18 00:00')
        self.get_current_stage_end_time_set_time('2022-08-15 02:00', '2022-08-18 00:00')
        self.get_current_stage_end_time_set_time('2022-08-16 02:00', '2022-08-18 00:00')
        self.get_current_stage_end_time_set_time('2022-08-17 02:00', '2022-08-18 00:00')
        self.get_current_stage_end_time_set_time(
            '2022-08-17 23:59:59', '2022-08-18 00:00'
        )

        self.get_current_stage_end_time_set_time(
            '2022-08-18 00:00:01', '2022-08-21 00:00'
        )
        self.get_current_stage_end_time_set_time(
            '2022-08-19 00:00:01', '2022-08-21 00:00'
        )
        self.get_current_stage_end_time_set_time(
            '2022-08-20 00:00:01', '2022-08-21 00:00'
        )
        self.get_current_stage_end_time_set_time(
            '2022-08-20 10:00:01', '2022-08-21 00:00'
        )
        self.get_current_stage_end_time_set_time(
            '2022-08-20 10:00:01', '2022-08-21 00:00'
        )

        self.get_current_stage_end_time_set_time(
            '2022-08-21 00:00:01', '2022-08-22 00:00'
        )
        self.get_current_stage_end_time_set_time('2022-08-21 00:04', '2022-08-22 00:00')
        self.get_current_stage_end_time_set_time('2022-08-21 15:04', '2022-08-22 00:00')
        self.get_current_stage_end_time_set_time(
            '2022-08-21 23:59:59', '2022-08-22 00:00'
        )
