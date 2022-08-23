from rest_framework import permissions

from api.control.models import Stage


class IsEvaluationAcceptingStage(permissions.BasePermission):
    """
    Проверяет совпадение текущего этапа с этапом приёма проверок..
    """

    message = f"Ошибка текущего этапа. Для отправки проверки необходим '{Stage.StagesEnum.EVALUATION_ACCEPTING}' этап."

    def has_permission(self, request, view) -> bool:
        return Stage.get_stage() == Stage.StagesEnum.EVALUATION_ACCEPTING
