from rest_framework import generics, permissions

from .models import Text
from .serializers import TextCreateSerializer, TextListSerializer, TextDetailSerializer


class TextCreate(generics.CreateAPIView):
    serializer_class = TextCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class TextListView(generics.ListAPIView):
    queryset = Text.objects.all()
    serializer_class = TextListSerializer
    permission_classes = [permissions.IsAdminUser]


class TextDetailView(generics.RetrieveUpdateAPIView):
    queryset = Text.objects.all()
    serializer_class = TextDetailSerializer
    permission_classes = [permissions.IsAdminUser]
