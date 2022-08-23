from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from ..models import Text, TextKey
from api.models import User


class TextsTest(APITestCase):
    def setUp(self) -> None:
        call_command('init_stage')
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.common_user = User.objects.create_user(username='common_user')
        self.admin_user = User.objects.create_superuser(username='test_admin')

    @staticmethod
    def get_teacher_uuid() -> str:
        return User.objects.create_superuser(username='test_admin_teacher').id

    def test_anon_text_assign(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid(),
        }
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Text.objects.all().count(), 0)

    def test_auth_user_text_assign(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid(),
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}'
        )
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Text.objects.all().count(), 0)

    def test_admin_user_text_assign(self):
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
        self.assertEqual(Text.objects.all().count(), 1)
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Text.objects.all().count(), 2)

    def test_anon_user_texts_list_all(self):
        response = self.client.get(reverse('texts_list_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_common_user_texts_list_all(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}'
        )
        response = self.client.get(reverse('texts_list_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_texts_list_all(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.get(reverse('texts_list_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 0)

    def test_admin_user_texts_list_all_with_texts(self):
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
        self.assertEqual(Text.objects.all().count(), 1)

        response = self.client.get(reverse('texts_list_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)

        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Text.objects.all().count(), 2)

        response = self.client.get(reverse('texts_list_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

    def test_admin_user_add_text_keys_empty(self):
        data = {"range_of_problems": "", "authors_position": "", "text": None}
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.post(reverse('add_text_keys'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TextKey.objects.all().count(), 0)

    def test_admin_user_add_text_keys_good(self):
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
        self.assertEqual(Text.objects.all().count(), 1)
        text_id = response.json()['id']
        self.assertIsNotNone(text_id)

        self.assertEqual(TextKey.objects.all().count(), 0)
        data = {
            "range_of_problems": "wkjeuhweriohiowg",
            "authors_position": "weiuguiweunguweugowegwenguweohigwegwe",
            "text": text_id,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.post(reverse('add_text_keys'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TextKey.objects.all().count(), 1)

    def test_admin_user_add_text_keys_good_many(self):
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
        self.assertEqual(Text.objects.all().count(), 1)
        text_id = response.json()['id']
        self.assertIsNotNone(text_id)

        self.assertEqual(TextKey.objects.all().count(), 0)
        data = {
            "range_of_problems": "wkjeuhweriohiowg",
            "authors_position": "weiuguiweunguweugowegwenguweohigwegwe",
            "text": text_id,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.post(reverse('add_text_keys'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TextKey.objects.all().count(), 1)

        data = {
            "range_of_problems": "289f2jivo",
            "authors_position": "ogjroigjo3jop[g3p",
            "text": text_id,
        }
        response = self.client.post(reverse('add_text_keys'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TextKey.objects.all().count(), 2)
