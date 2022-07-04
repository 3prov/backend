from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Stage
from rest_framework import permissions


class StageAddView(APIView):

    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        return JsonResponse({
            'current_stage': Stage.get_stage(),
            'possible_stages': [{x[0]: x[1]} for x in Stage.StagesEnum.choices],
        })


class SwitchStageAddView(APIView):

    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        return JsonResponse({
            'current_stage': Stage.switch_stage_to_next(),
            'possible_stages': [{x[0]: x[1]} for x in Stage.StagesEnum.choices],
        })
