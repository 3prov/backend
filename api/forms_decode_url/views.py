from django.urls import reverse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.form_url.models import EssayFormURL, EvaluationFormURL
from api.management.models import WeekID
from api.rus.essays.permissions import IsWorkAcceptingStage
from api.rus.essays.serializers import EssaySerializer
from api.rus.evaluations.models import EssayEvaluation
from api.rus.evaluations.serializers import EssayEvaluationSerializer
from api.rus.models import Essay, Text, TextKey
from api.rus.texts.serializers import TextSerializer, TextKeySerializer


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
                'essay': False,
            },
            'task': False,
        }

        form_url = EssayFormURL.get_from_url(kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )

        data_to_response['task'] = TextSerializer(Text.get_current()).data
        try:
            essay = Essay.objects.get(
                author=form_url.user, task__week_id=WeekID.get_current()
            )
            data_to_response['work_already_sent'] = True
            data_to_response['work']['essay'] = EssaySerializer(essay).data
            data_to_response['urls']['to_PATCH'] = reverse(
                'essay_from_url_edit', args=[form_url.url]
            )
        except Essay.DoesNotExist:
            data_to_response['urls']['to_POST'] = reverse(
                'essay_from_url_post', args=[form_url.url]
            )

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
            'evaluation': False,
            'task': False,
            'task_keys': False,
        }

        form_url = EvaluationFormURL.get_from_url(kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )

        _current_text = Text.get_current()
        data_to_response['task'] = TextSerializer(_current_text).data
        data_to_response['task_keys'] = TextKeySerializer(
            TextKey.objects.filter(text=_current_text), many=True
        ).data
        try:
            evaluation = EssayEvaluation.objects.get(
                evaluator=form_url.user, work=form_url.evaluation_work
            )
            data_to_response['evaluation_already_sent'] = True
            data_to_response['evaluation'] = EssayEvaluationSerializer(evaluation).data
            data_to_response['urls']['to_PATCH'] = reverse(
                'evaluation_from_url_edit', args=[form_url.url]
            )  # TODO: change serializer
        except EssayEvaluation.DoesNotExist:
            data_to_response['urls']['to_POST'] = reverse(
                'evaluation_from_url_post', args=[form_url.url]
            )

        return Response(data_to_response)
