from rest_framework import generics, permissions
from rest_framework.views import APIView

from ..models import Essay
from .serializers import (
    EssayCreateSerializer,
    EssayListSerializer,
    EssayDetailSerializer,
    EssayGetLinkToFormCreateSerializer
)
from .permissions import OwnUserPermission, IsWorkAcceptingStage, IsWorkAlreadyExists, IsFormURLAlreadyExists
from ...models import FormURL


class EssayCreate(generics.CreateAPIView):
    serializer_class = EssayCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkAcceptingStage, IsWorkAlreadyExists]


class EssayListView(generics.ListAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayListSerializer
    permission_classes = [permissions.IsAdminUser]


class EssayDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayDetailSerializer
    permission_classes = [OwnUserPermission, IsWorkAcceptingStage]


class EssayDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayDetailSerializer
    permission_classes = [OwnUserPermission, IsWorkAcceptingStage]


class EssayGetLinkToFormView(generics.CreateAPIView):
    serializer_class = EssayGetLinkToFormCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormURLAlreadyExists]


