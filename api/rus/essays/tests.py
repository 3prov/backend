from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from ..models import Text, TextKey, Essay
from api.models import User, FormURL
from ...management import init_stage


class EssaysTest(APITestCase):

    def setUp(self) -> None:
        init_stage()
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.common_user = User.objects.create_user(username='common_user')
        self.admin_user = User.objects.create_superuser(username='test_admin')
        self.assign_text()


    @staticmethod
    def get_teacher_uuid() -> str:
        return User.objects.create_superuser(username='test_admin_teacher').id

    def assign_text(self):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.get_teacher_uuid()
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}')
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Text.objects.all().count(), 1)

    def test_anon_pass_essay(self):
        data = {
            'body': 'f09muf8ni8y83yof8y3f83fm3uf3m9f3pf93nfp93f93nf83pf3npf 3pf3f3ou389o3  33pf3f3',
            'author': self.common_user.id
        }
        response = self.client.post(reverse('essay_pass'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def pass_essay(self, user):
        data = {
            'body': 'f09muf8ni8y83yof8y3f83fm3uf3m9f3pf93nfp93f93nf83pf3npf 3pf3f3ou389o3  33pf3f3',
            'author': user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
        return self.client.post(reverse('essay_pass'), data, format='json')

    def test_common_pass_essay_wrong_stage_before(self):
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'],
                         "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.")

    def switch_stage(self, user_to_return):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}')
        self.client.get(reverse('switch_stage_to_next'))
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_to_return.auth_token}')

    def test_common_pass_essay_good_state(self):
        self.assertEqual(Essay.objects.all().count(), 0)
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json()['id'])
        self.assertIsNotNone(response.json()['task'])
        self.assertIsNotNone(response.json()['body'])
        self.assertEqual(Essay.objects.all().count(), 1)

    def test_common_pass_essay_good_state_more_than_one_pass(self):
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.pass_essay(self.common_user)
        self.assertEqual(Essay.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 1)

    def test_common_pass_essay_wrong_stage_after(self):
        self.switch_stage(self.common_user)
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'],
                         "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.")
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'],
                         "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.")
        self.switch_stage(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'],
                         "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.")
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_essay_patch(self):
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)

        data = {
            'id': response.json()['id'],
            'body': 'new body'
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}')
        response = self.client.patch(reverse('essay_detail', args=[data['id']]), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], data['id'])
        self.assertEqual(response.json()['body'], data['body'])

    def test_essay_patch_wrong_stage(self):
        self.switch_stage(self.common_user)
        response = self.pass_essay(self.common_user)
        self.switch_stage(self.common_user)

        data = {
            'id': response.json()['id'],
            'body': 'new body'
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}')
        response = self.client.patch(reverse('essay_detail', args=[data['id']]), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'],
                         "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.")

    def test_get_link_to_form(self):
        self.switch_stage(self.common_user)
        data = {
            'user': self.common_user.id
        }
        self.assertEqual(FormURL.objects.all().count(), 0)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}')
        response = self.client.post(reverse('essay_get_link_to_form'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json()['url'])
        self.assertEqual(len(response.json()['url']), 16)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(FormURL.objects.all().count(), 1)
        self.assertEqual(response.json()['user'], str(self.common_user.id))

    def test_get_link_to_form_more_times(self):
        self.switch_stage(self.common_user)
        data = {
            'user': self.common_user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}')
        response = self.client.post(reverse('essay_get_link_to_form'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('essay_get_link_to_form'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(FormURL.objects.all().count(), 1)
        self.assertEqual(response.json()['detail'], 'Ссылка на форму уже выдана.')

