from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.form_url.models import EssayFormURL, EvaluationFormURL
from api.control.models import WeekID
from api.rus.essays.permissions import IsWorkAcceptingStage
from api.rus.essays.serializers import EssaySerializer
from api.rus.evaluations.models import EssayEvaluation
from api.rus.evaluations.serializers import EssayEvaluationSerializer
from api.rus.models import Essay, Text, TextKey
from api.rus.texts.serializers import TextSerializer, TextKeySerializer
from api.services import filter_objects, get_object


class EssayDecodeURLView(APIView):

    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage]

    def get(self, request, *args, **kwargs):
        data_to_response = {
            'essay_already_sent': False,
            'essay': None,
            'task': None,
        }

        form_url = EssayFormURL.get_from_url_or_404(kwargs['encoded_part'])
        data_to_response['task'] = TextSerializer(Text.get_current()).data
        try:
            essay = get_object(
                Essay.objects, author=form_url.user, task__week_id=WeekID.get_current()
            )
            data_to_response['essay_already_sent'] = True
            data_to_response['essay'] = EssaySerializer(essay).data
        except Essay.DoesNotExist:
            pass

        return Response(data_to_response)


class EvaluationDecodeURLView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data_to_response = {
            'evaluation_already_sent': False,
            'evaluation': None,
            'essay': None,
            'task': None,
            'task_keys': None,
        }

        form_url = EvaluationFormURL.get_from_url_or_404(kwargs['encoded_part'])
        _current_text = Text.get_current()
        data_to_response['essay'] = EssaySerializer(form_url.evaluation_work).data
        data_to_response['task'] = TextSerializer(_current_text).data
        data_to_response['task_keys'] = TextKeySerializer(
            filter_objects(
                TextKey.objects,
                text=_current_text,
            ),
            many=True,
        ).data
        try:
            evaluation = get_object(
                EssayEvaluation.objects,
                evaluator=form_url.user,
                work=form_url.evaluation_work,
            )
            data_to_response['evaluation_already_sent'] = True
            data_to_response['evaluation'] = EssayEvaluationSerializer(evaluation).data
        except EssayEvaluation.DoesNotExist:
            pass

        return Response(data_to_response)
