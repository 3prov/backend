from uuid import UUID

from django.core.management import call_command
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
    override_settings,
)

from ..models import Text, Essay
from api.models import User
from ...form_url.models import EssayFormURL


class EssaysTest(APITestCase):
    def setUp(self) -> None:
        call_command('init_stage')
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.common_user = User.objects.create_user(username='common_user')
        self.common_user_2 = User.objects.create_user(username='common_user_2')
        self.common_user_3 = User.objects.create_user(username='common_user_3')
        self.common_user_4 = User.objects.create_user(username='common_user_4')

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
            "teacher": self.get_teacher_uuid(),
        }
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        response = self.client.post(reverse('text_assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Text.objects.all().count(), 1)

    def get_or_create_essay_form_link(self, user):
        data = {'user': user.id}
        return self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )

    def pass_essay(self, user, form_url_url: str):
        data = {'body': f'essay from {user.username}!'}
        return self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )

    def switch_stage(self, user_to_return):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}'
        )
        self.client.get(reverse('switch_stage_to_next'))
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_to_return.auth_token}')

    def test_get_or_create_essay_form_link_wrong_uuid(self):
        data = {'user': 'b1064f74-6db4-44a5-89b5-187790df9b5s'}
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'user': '123'}
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_common_pass_essay_good_state(self):
        self.assertEqual(Essay.objects.all().count(), 0)
        self.switch_stage(self.common_user)
        response = self.get_or_create_essay_form_link(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EssayFormURL.objects.all().count(), 1)
        response_p1 = self.pass_essay(self.common_user, response.json()['url'])
        self.assertEqual(response_p1.status_code, status.HTTP_201_CREATED)
        response_p2 = self.pass_essay(self.common_user, response.json()['url'])
        self.assertEqual(response_p2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 1)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_common_pass_essay_wrong_stage_after(self):
        self.switch_stage(self.common_user)
        self.switch_stage(self.common_user)
        response = self.get_or_create_essay_form_link(self.common_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_p1 = self.pass_essay(self.common_user, response.json()['url'])
        self.assertEqual(response_p1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response_p1.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )
        self.switch_stage(self.common_user)
        response_p1 = self.pass_essay(self.common_user, response.json()['url'])
        self.assertEqual(response_p1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(response_p1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_p1.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )
        self.switch_stage(self.common_user)
        response_p1 = self.pass_essay(self.common_user, response.json()['url'])
        self.assertEqual(response_p1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response_p1.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )
        self.switch_stage(self.common_user)
        response_p1 = self.pass_essay(self.common_user, response.json()['url'])
        self.assertEqual(response_p1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Essay.objects.all().count(), 1)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_get_link_to_form(self):
        self.switch_stage(self.common_user)
        data = {'user': self.common_user.id}
        self.assertEqual(EssayFormURL.objects.all().count(), 0)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}'
        )
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json()['url'])
        self.assertEqual(len(response.json()['url']), 16)
        # self.assertEqual(response.json()['id'], 1)
        self.assertEqual(EssayFormURL.objects.all().count(), 1)
        self.assertEqual(response.json()['user'], str(self.common_user.id))

    def test_get_link_to_form_more_times(self):
        self.switch_stage(self.common_user)
        data = {'user': self.common_user.id}
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}'
        )
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(EssayFormURL.objects.all().count(), 1)
        self.assertEqual(UUID(response.json()['user']), data['user'])

    def test_pass_essay_by_form_url_link_common_user(self):
        self.switch_stage(self.common_user)
        data = {'user': self.common_user.id}
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.common_user.auth_token}'
        )
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        form_url_url = response.json()['url']
        data = {'body': 'essay from common user!'}
        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Essay.objects.all().count(), 1)

        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 1)
        self.assertEqual(
            response.json()['detail'], 'Сочинение на этой неделе уже существует.'
        )

    def test_pass_essay_by_form_url_link_anon_user_without_creds(self):
        self.switch_stage(self.common_user)
        data = {'user': self.common_user.id}
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        form_url_url = response.json()['url']
        data = {'body': 'essay from common user!'}
        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Essay.objects.all().count(), 1)

        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 1)
        self.assertEqual(
            response.json()['detail'], 'Сочинение на этой неделе уже существует.'
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_pass_essay_by_form_url_link_common_user_wrong_stage(self):
        data = {'user': self.common_user.id}
        response = self.client.post(
            reverse('get_or_create_essay_form_link'), data, format='json'
        )
        form_url_url = response.json()['url']
        data = {'body': 'essay from common user!'}
        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )

        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )

        self.switch_stage(self.common_user)  # to S2
        self.switch_stage(self.common_user)  # to S3
        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )
        self.switch_stage(self.common_user)  # to S4
        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )
        self.switch_stage(self.common_user)  # to S1
        response = self.client.post(
            reverse('essay_from_url_post', args=[form_url_url]), data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Essay.objects.all().count(), 0)
        self.assertEqual(
            response.json()['detail'],
            "Ошибка текущего этапа. Для отправки сочинения необходим 'S2' этап.",
        )
