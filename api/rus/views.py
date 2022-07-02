from rest_framework import generics, permissions
from .serializers import TextCreateSerializer


class TextCreate(generics.CreateAPIView):
    serializer_class = TextCreateSerializer
    permission_classes = [permissions.IsAdminUser]
