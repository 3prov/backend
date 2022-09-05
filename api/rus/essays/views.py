from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Essay
from .serializers import (
    EssayListSerializer,
    EssayFormSerializer,
    EssayFormURLCreateSerializer,
    EssayWithEvaluationsSerializer,
)
from .permissions import (
    IsWorkAcceptingStage,
    IsWorkDoesNotAlreadyExistsFromFormURL,
)
from ...form_url.models import EssayFormURL
from ...control.models import WeekID
from ...models import User


class EssayListView(generics.ListAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayListSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'task__week_id__study_year_from',
        'task__week_id',
    ]  # TODO: `task__week_id` is id


class EssayFormURLUserGetOrCreate(generics.CreateAPIView):
    serializer_class = EssayFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serialized = self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        form_url, is_created = EssayFormURL.objects.get_or_create(
            week_id=WeekID.get_current(),
            user_id=request.data['user'],
        )
        return Response(
            self.get_serializer(form_url).data,
            status=status.HTTP_201_CREATED if is_created else status.HTTP_200_OK,
        )


class EssayWithEvaluationsTextKeysView(generics.RetrieveAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayWithEvaluationsSerializer
    permission_classes = [permissions.AllowAny]


class EssayFromFormURLCreate(generics.CreateAPIView):
    queryset = EssayFormURL.objects.all()
    serializer_class = EssayFormURLCreateSerializer
    permission_classes = [
        permissions.AllowAny,
        IsWorkAcceptingStage,
        IsWorkDoesNotAlreadyExistsFromFormURL,
    ]

    def create(self, request, *args, **kwargs):
        form_url = EssayFormURL.get_from_url_or_404(url=kwargs['encoded_part'])
        added_essay = Essay.objects.create(
            task=form_url.week_id.task, body=request.data['body'], author=form_url.user
        )
        return Response(
            self.get_serializer(added_essay).data,
            status=status.HTTP_201_CREATED,
        )


class EssayFromFormURLDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage]
    serializer_class = EssayFormURLCreateSerializer

    def get_object(self):
        form_url = EssayFormURL.get_from_url_or_404(url=self.kwargs['encoded_part'])
        queryset = self.get_queryset()
        return get_object_or_404(
            queryset, author=form_url.user, task__week_id=form_url.week_id
        )
