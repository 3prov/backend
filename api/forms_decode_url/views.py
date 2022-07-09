from django.urls import reverse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.form_url.models import EssayFormURL, EvaluationFormURL
from api.management.models import WeekID
from api.rus.essays.permissions import IsWorkAcceptingStage
from api.rus.evaluations.models import EssayEvaluation
from api.rus.evaluations.serializers import EssayEvaluationDetailSerializer
from api.rus.models import Essay


class EssayDecodeURLView(APIView):

    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage]

    def get(self, request, *args, **kwargs):
        data_to_response = {
            'work_already_sent': False,
            'urls': {
                'to_POST': False,
                'to_PATCH': False,
            },
            'work': {
                'essay_body': False,
            },
        }

        form_url = EssayFormURL.get_from_url(kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})

        try:
            essay = Essay.objects.get(author=form_url.user, task__week_id=WeekID.get_current())
            data_to_response['work_already_sent'] = True
            data_to_response['work']['essay_body'] = essay.body
            data_to_response['urls']['to_PATCH'] = reverse('essay_from_url_edit', args=[form_url.url])
        except Essay.DoesNotExist:
            data_to_response['urls']['to_POST'] = reverse('essay_from_url_post', args=[form_url.url])

        return Response(data_to_response)


class EvaluationDecodeURLView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data_to_response = {
            'evaluation_already_sent': False,
            'urls': {
                'to_POST': False,
                'to_PATCH': False,
            },
            'evaluation': {
                'body': False,
            },
        }

        form_url = EvaluationFormURL.get_from_url(kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})

        try:
            evaluation = EssayEvaluation.objects.get(evaluator=form_url.user, work=form_url.evaluation_work)
            data_to_response['evaluation_already_sent'] = True
            print(f'{EssayEvaluationDetailSerializer(evaluation).is_valid()=}')
        except EssayEvaluation.DoesNotExist:
            data_to_response['urls']['to_POST'] = 214

        # try:
        #     essay = Essay.objects.get(author=form_url.user)
        #     data_to_response['work_already_sent'] = True
        #     data_to_response['work']['essay_body'] = essay.body
        #     data_to_response['urls']['to_PATCH'] = reverse('essay_detail', args=[essay.id])
        # except Essay.DoesNotExist:
        #     data_to_response['urls']['to_POST'] = reverse('essay_from_url_post', args=[form_url.url])

        return Response(data_to_response)
