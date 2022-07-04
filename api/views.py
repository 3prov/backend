from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes

from .models import User
from .serializers import UserListSerializer, UserDetailSerializer


@api_view()
@permission_classes([permissions.AllowAny])
def health_check_view(request):
    return Response({"health": "OK"})


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        users = User.objects.all()
        return users


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]

