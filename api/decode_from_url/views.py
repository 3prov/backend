from django.urls import reverse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import FormURL
from api.rus.models import Essay


class DecodeURLView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data_to_response = {
            'form_type': {
                'is_essay_form': False,
                'is_check_form': False,
            },
            'already_sent': False,
            'urls': {
                'to_POST': False,
                'to_PATCH': False,
            },
            'work': {
                'essay_body': False,
                'check': {
                    'body': False,
                    'k1': {
                        'score': False,
                        'comment': False,
                    },
                    'k2': {
                        'score': False,
                        'comment': False,
                    },  # TODO: k3, k4.., k12
                }
            },
        }

        form_url = FormURL.get_from_url(kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})

        try:
            essay = Essay.objects.get(author=form_url.user)
            data_to_response['already_sent'] = True
            data_to_response['work']['essay_body'] = essay.body
            data_to_response['urls']['to_PATCH'] = reverse('essay_detail', args=[essay.id])
        except Essay.DoesNotExist:
            data_to_response['form_type']['is_essay_form'] = True  # TODO: fix it
            data_to_response['urls']['to_POST'] = reverse('essay_from_url_post', args=[form_url.url])

        return Response(data_to_response)

