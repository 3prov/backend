from rest_framework import generics, permissions

from ..models import Essay
from .serializers import EssayCreateSerializer, EssayListSerializer, EssayDetailSerializer


class EssayCreate(generics.CreateAPIView):
    serializer_class = EssayCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class EssayListView(generics.ListAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayListSerializer
    permission_classes = [permissions.IsAdminUser]


class EssayDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayDetailSerializer
    permission_classes = [permissions.IsAdminUser]
