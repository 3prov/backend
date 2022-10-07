from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes

from .models import User
from .serializers import UserListSerializer, UserActiveSerializer
from .services import all_objects


@api_view()
@permission_classes([permissions.AllowAny])
def health_check_view(request):
    return Response({"health": "OK"})


class UserListView(generics.ListAPIView):
    queryset = all_objects(User.objects)
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]


class UserActiveView(generics.RetrieveUpdateAPIView):
    queryset = all_objects(User.objects)
    serializer_class = UserActiveSerializer
    permission_classes = [permissions.IsAdminUser]
