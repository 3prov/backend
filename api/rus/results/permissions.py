from rest_framework import permissions

from api.form_url.models import ResultsFormURL
from api.management.models import WeekID
from api.rus.results.serializers import WeekResultsFormCreateSerializer


class IsWeekResultsFormURLAlreadyExists(permissions.BasePermission):
    """
    Проверяет, чтобы пользователь мог получить не более одной ссылки на форму.
    """

    message = "Ссылка на форму уже выдана."

    def has_permission(self, request, view) -> bool:
        serialized = WeekResultsFormCreateSerializer(data=request.data)
        if not serialized.is_valid():
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ошибка сериализации данных.'}
            )
        current_week_id = WeekID.get_current()
        already_given_url = ResultsFormURL.objects.filter(
            user_id=request.data['user'], week_id=current_week_id
        )
        return not already_given_url.exists()
