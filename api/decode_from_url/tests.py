from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from ..management import init_stage
from ..models import User


class ManagementTest(APITestCase):

    def setUp(self) -> None:
        init_stage()
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin_user')
        self.common_user = User.objects.create_user(username='common_user')

    def assign_text(self, user_to_return):
        data = {
            "body": "inu2fg38",
            "author": "92m8yn823",
            "author_description": "g2yn8g2y3g923",
            "teacher": self.admin_user.id
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}')
        self.client.post(reverse('text_assign'), data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_to_return.auth_token}')

    def switch_stage(self, user_to_return):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_user.auth_token}')
        self.client.get(reverse('switch_stage_to_next'))
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_to_return.auth_token}')

    def get_link_to_form(self, user) -> str:
        data = {
            'user': user.id
        }
        return self.client.post(reverse('essay_get_link_to_form'), data, format='json').json()['url']

    def test_simulate(self):
        self.assign_text(self.common_user)
        self.switch_stage(self.common_user)
        encoded_url = self.get_link_to_form(self.common_user)
        response = self.client.get(reverse('form_distribution_by_encoded_part', args=[encoded_url]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['already_sent'], False)
        to_post_url = response.json()['urls']['to_POST']
        to_patch_url = response.json()['urls']['to_PATCH']
        self.assertNotEqual(to_post_url, False)
        self.assertEqual(to_patch_url, False)
        data = {
            'body': 'тест.'
        }
        response = self.client.post(to_post_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('form_distribution_by_encoded_part', args=[encoded_url]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['already_sent'], True)
        to_post_url = response.json()['urls']['to_POST']
        to_patch_url = response.json()['urls']['to_PATCH']
        self.assertEqual(to_post_url, False)
        self.assertNotEqual(to_patch_url, False)
        self.assertEqual(response.json()['work']['essay_body'], data['body'])


        data = {
            'body': 'теперь измененное содержимое!'
        }
        response = self.client.patch(to_patch_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('form_distribution_by_encoded_part', args=[encoded_url]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['already_sent'], True)
        to_post_url = response.json()['urls']['to_POST']
        to_patch_url = response.json()['urls']['to_PATCH']
        self.assertEqual(to_post_url, False)
        self.assertNotEqual(to_patch_url, False)
        self.assertEqual(response.json()['work']['essay_body'], data['body'])

        # TODO: test check urls
