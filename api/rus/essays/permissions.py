from rest_framework import exceptions, permissions

from ..models import Essay, Text
from ...form_url.models import EssayFormURL
from ...management.models import Stage, WeekID
from .serializers import (
    EssayCreateSerializer,
    EssayFormSerializer,
    EssayFormURLCreateSerializer,
)
from ...models import User


class OwnUserPermission(permissions.BasePermission):
    """
    Позволяет изменять работу только его автору (и админам).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        user_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not user_token:
            return False
        if not user_token.startswith('Token '):
            return False
        user_token = user_token.replace('Token ', '')

        try:
            user_with_token = User.objects.get(auth_token=user_token)
        except User.DoesNotExist:
            return False
        return obj.author == user_with_token


class IsWorkAcceptingStage(permissions.BasePermission):
    """
    Проверяет совпадение текущего этапа с этапом приёма работ.
    """

    message = f"Ошибка текущего этапа. Для отправки сочинения необходим '{Stage.StagesEnum.WORK_ACCEPTING}' этап."

    def has_permission(self, request, view) -> bool:
        if Stage.get_stage() != Stage.StagesEnum.WORK_ACCEPTING:
            raise exceptions.PermissionDenied(detail=self.message)
        return True


class IsWorkDoesNotAlreadyExists(permissions.BasePermission):
    """
    Проверяет, чтобы пользователь мог отправить не более одной работы за одну волну (неделю).
    """

    message = "Сочинение на этой неделе уже существует."

    def has_permission(self, request, view) -> bool:
        serialized = EssayCreateSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        current_text = Text.get_current()
        already_sent_essay = Essay.objects.filter(
            author=serialized.data['author'], task=current_text
        )
        return not already_sent_essay.exists()


class IsEssayFormURLAlreadyExists(permissions.BasePermission):
    """
    Проверяет, чтобы пользователь мог получить не более одной ссылки на форму.
    """

    message = "Ссылка на форму уже выдана."

    def has_permission(self, request, view) -> bool:
        serialized = EssayFormSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        current_week_id = WeekID.get_current()
        already_given_url = EssayFormURL.objects.filter(
            user_id=request.data['user'], week_id=current_week_id
        )
        return not already_given_url.exists()


class IsWorkDoesNotAlreadyExistsFromFormURL(permissions.BasePermission):
    """
    Проверяет, чтобы пользователь мог отправить не более одной работы за одну волну (неделю).
    Принимает данные по ссылкам FormURL.
    """

    message = "Сочинение на этой неделе уже существует."

    def has_permission(self, request, view) -> bool:
        serializer = EssayFormURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_text = Text.get_current()
        form_url = EssayFormURL.get_from_url(view.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )
        already_sent_essay = Essay.objects.filter(
            author=form_url.user, task=current_text
        )
        return not already_sent_essay.exists()
