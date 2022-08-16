from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Stage
from rest_framework import permissions

from .utils import ManagementUtils
from ..rus.models import Essay, Text


class StageAddView(APIView):

    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        return JsonResponse(
            {
                'current_stage': Stage.get_stage(),
                'possible_stages': [{x[0]: x[1]} for x in Stage.StagesEnum.choices],
            }
        )


class SwitchStageAddView(APIView):

    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        return JsonResponse(
            {
                'current_stage': Stage.switch_stage_to_next(),
                'possible_stages': [{x[0]: x[1]} for x in Stage.StagesEnum.choices],
            }
        )


class StatisticsAddView(APIView):

    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        return JsonResponse(
            {
                'rus': {
                    'essays_passed': Essay.objects.filter(
                        task=Text.get_current()
                    ).count(),
                }
            }
        )


class CurrentStageEndTime(APIView):

    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        return JsonResponse(
            {
                'current_stage': Stage.get_stage(),
                'time': {
                    'server_current': ManagementUtils.get_current_time().isoformat(),
                    'stage_end': Stage.get_current_stage_end_time().isoformat(),
                },
            }
        )
