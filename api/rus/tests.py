from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from .models import Text
from ..models import User


class ManagementTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    @staticmethod
    def get_teacher_uuid() -> str:
        return User.objects.create_superuser(username='test_admin_teacher').id

    def test_anon_text_assign(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid()
        }
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Text.objects.all().count(), 0)

    def test_auth_user_text_assign(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid()
        }
        common_user = User.objects.create_user(username='common_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {common_user.auth_token}')
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Text.objects.all().count(), 0)

    def test_admin_user_text_assign(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid()
        }
        admin_user = User.objects.create_superuser(username='test_admin')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token}')
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Text.objects.all().count(), 1)
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Text.objects.all().count(), 2)

