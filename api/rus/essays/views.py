from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Essay, Text
from .serializers import (
    EssayCreateSerializer,
    EssayListSerializer,
    EssayDetailSerializer,
    EssayFormCreateSerializer,
    EssayFormURLCreateSerializer,
)
from .permissions import (
    OwnUserPermission,
    IsWorkAcceptingStage,
    IsWorkDoesNotAlreadyExists,
    IsEssayFormURLAlreadyExists,
    IsWorkDoesNotAlreadyExistsFromFormURL,
)
from ...form_url.models import EssayFormURL
from ...management.models import WeekID


class EssayCreate(generics.CreateAPIView):
    serializer_class = EssayCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkAcceptingStage, IsWorkDoesNotAlreadyExists]


class EssayListView(generics.ListAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayListSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task__week_id__study_year_from', 'task__week_id']  # TODO: `task__week_id` is id


class EssayFormURLUserCreate(generics.CreateAPIView):
    serializer_class = EssayFormCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEssayFormURLAlreadyExists]


class EssayDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayDetailSerializer
    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage]


class EssayFromFormURLCreate(generics.CreateAPIView):
    queryset = EssayFormURL.objects.all()
    serializer_class = EssayFormURLCreateSerializer
    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage, IsWorkDoesNotAlreadyExistsFromFormURL]

    def create(self, request, *args, **kwargs):
        form_url = EssayFormURL.get_from_url(url=kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})
        added_essay = Essay.objects.create(
            task=Text.get_current(),
            body=request.data['body'],
            author=form_url.user
        )
        return Response(EssayFormURLCreateSerializer(added_essay).data, status=status.HTTP_201_CREATED)  # TODO: change EssayFormURLCreateSerializer


class EssayFormURLUserListView(generics.ListAPIView):
    serializer_class = EssayFormCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return EssayFormURL.objects.filter(user=self.kwargs['user'], week_id=WeekID.get_current())


class EssayFromFormURLDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage]
    serializer_class = EssayDetailSerializer

    def get_object(self):
        form_url = EssayFormURL.get_from_url(url=self.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, author=form_url.user, task__week_id=form_url.week_id)
        return obj
