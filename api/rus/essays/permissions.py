from rest_framework import exceptions, permissions

from ..models import Essay, Text
from ...form_url.models import EssayFormURL
from ...control.models import Stage
from .serializers import (
    EssayFormURLCreateSerializer,
)
from ...models import User
from ...services import filter_objects


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
        form_url = EssayFormURL.get_from_url_or_404(view.kwargs['encoded_part'])
        already_sent_essay = filter_objects(
            Essay.objects, author=form_url.user, task=current_text
        )
        return not already_sent_essay.exists()
