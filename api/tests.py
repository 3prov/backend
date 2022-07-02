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
        self.assertEqual(User.objects.all().count(), 1)
        self.assertNotEqual('p@ssw0rd', user.password)
        self.assertTrue(user.is_active)
        user.delete()
        self.assertEqual(User.objects.all().count(), 0)

    def test_check_user_from_api(self):
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

        data['username'] = 'username1'
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 0)

        data['password'] = 'JohnPassword'
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)

        data['username'] = 'username2'
        data['vkontakte_id'] = 157651005
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(User.objects.get(username='username2').vkontakte_id, 157651005)
        self.assertIsNone(User.objects.get(username='username2').telegram_id)

        data['username'] = 'username2'
        data['vkontakte_id'] = 157651006
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 2)

        data['username'] = 'username3'
        data['vkontakte_id'] = 157651007
        data['telegram_id'] = 189245914
        response = self.client.post(reverse('user-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 3)
        self.assertEqual(User.objects.get(username='username3').vkontakte_id, 157651007)
        self.assertEqual(User.objects.get(username='username3').telegram_id, 189245914)

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
        self.assertEqual(User.objects.all().count(), 4)
        self.assertNotEqual(User.objects.get(username='username_full').password, 'aboba22')
        self.assertEqual(User.objects.get(username='username_full').first_name, 'John')
        self.assertEqual(User.objects.get(username='username_full').last_name, 'Doe')
        self.assertEqual(User.objects.get(username='username_full').vkontakte_id, 6127584)
        self.assertEqual(User.objects.get(username='username_full').telegram_id, 891267646512)
        self.assertIsNotNone(User.objects.get(username='username2').id)

