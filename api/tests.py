from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from .models import User


class UserTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_check_user_from_model(self):
        user = User.objects.create_user('username', 'p@ssw0rd')
        self.assertIsNotNone(user.auth_token)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertNotEqual('p@ssw0rd', user.password)
        self.assertTrue(user.is_active)
        user.delete()
        self.assertEqual(User.objects.all().count(), 0)

    def test_check_user_from_api_empty(self):
        data = {
            "username": "",
            "password": "",
            "first_name": "",
            "last_name": "",
            "vkontakte_id": None,
            "telegram_id": None,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 0)

    def test_check_user_from_api_with_username(self):
        data = {
            "username": 'username1',
            "password": "",
            "first_name": "",
            "last_name": "",
            "vkontakte_id": None,
            "telegram_id": None,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 0)

    def test_check_user_from_api_with_username_and_password(self):
        data = {
            "username": 'username1',
            "password": 'JohnPassword',
            "first_name": "",
            "last_name": "",
            "vkontakte_id": None,
            "telegram_id": None,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertIsNotNone(User.objects.get(username='username1').auth_token)

    def test_check_user_from_api_with_username_and_password_and_vk(self):
        data = {
            "username": 'username1',
            "password": 'JohnPassword',
            "first_name": "",
            "last_name": "",
            "vkontakte_id": 157651005,
            "telegram_id": None,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.get(username='username1').vkontakte_id, 157651005)
        self.assertIsNone(User.objects.get(username='username1').telegram_id)
        self.assertIsNotNone(User.objects.get(username='username1').auth_token)

    def test_check_user_from_api_with_username_and_password_and_vk_double(self):
        data = {
            "username": 'username2',
            "password": 'JohnPassword',
            "first_name": "",
            "last_name": "",
            "vkontakte_id": 157651006,
            "telegram_id": None,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertIsNotNone(User.objects.get(username='username2').auth_token)

        data['username'] = 'username3'
        data['vkontakte_id'] = 157651007
        data['telegram_id'] = 189245914
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(User.objects.get(username='username3').vkontakte_id, 157651007)
        self.assertEqual(User.objects.get(username='username3').telegram_id, 189245914)
        self.assertIsNotNone(User.objects.get(username='username3').auth_token)

    def test_check_user_from_api_full_creds(self):
        data = {
            "username": "username_full",
            "password": "aboba22",
            "first_name": "John",
            "last_name": "Doe",
            "vkontakte_id": 6127584,
            "telegram_id": 891267646512,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertNotEqual(User.objects.get(username='username_full').password, 'aboba22')
        self.assertEqual(User.objects.get(username='username_full').first_name, 'John')
        self.assertEqual(User.objects.get(username='username_full').last_name, 'Doe')
        self.assertEqual(User.objects.get(username='username_full').vkontakte_id, 6127584)
        self.assertEqual(User.objects.get(username='username_full').telegram_id, 891267646512)
        self.assertIsNotNone(User.objects.get(username='username_full').id)
        self.assertIsNotNone(User.objects.get(username='username_full').auth_token)

    def test_check_user_from_api_wrong_serialized(self):
        data = {
            "username": "username_full",
            "password": "aboba22",
            "first_name": "John",
            "last_name": "Doe",
            "vkontakte_id": "6127584e",
            "telegram_id": 891267646512,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_user_from_api_wrong_serialized_2(self):
        data = {
            "username": "username_full",
            "password": "aboba22",
            "first_name": "John",
            "last_name": "Doe",
            "vkontakte_id": 6127584,
            "telegram_id": "wuiegf",
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_user_from_api_wrong_serialized_3(self):
        data = {
            "username": "username_full",
            "password": "aboba22",
            "first_name": "John",
            "last_name": "Doe",
            "vkontakte_id": "",
            "telegram_id": "",
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_user_from_api_wrong_serialized_4(self):
        data = {
            "username": "username_full",
            "password": "aboba22",
            "first_name": "John",
            "last_name": "Doe",
            "vkontakte_id": "",
            "telegram_id": None,
        }
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HealthTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_health_api(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['health'], "OK")
