from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from . import init_stage
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
        self.assertEqual(list(response.json()['current_stage'].keys())[0], 'S2')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(list(response.json()['current_stage'].keys())[0], 'S3')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(list(response.json()['current_stage'].keys())[0], 'S4')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(list(response.json()['current_stage'].keys())[0], 'S1')
        response = self.client.get(reverse('switch_stage_to_next'))
        self.assertEqual(list(response.json()['current_stage'].keys())[0], 'S2')

    def test_admin_user_switch_stage_to_next_many_times(self):
        admin_user = User.objects.create_superuser(username='test_admin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        responses_set = set()
        response = self.client.get(reverse('switch_stage_to_next'))
        prev = list(response.json()['current_stage'].keys())[0]
        for i in range(1, 30):
            response = self.client.get(reverse('switch_stage_to_next'))
            _key_stage = list(response.json()['current_stage'].keys())[0]
            responses_set.add(_key_stage)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertNotEqual(_key_stage, prev)
            prev = _key_stage
        self.assertEqual(len(responses_set), 4)


