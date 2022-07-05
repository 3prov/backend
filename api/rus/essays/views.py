from rest_framework import generics, permissions, status
from rest_framework.response import Response


from ..models import Essay, Text
from .serializers import (
    EssayCreateSerializer,
    EssayListSerializer,
    EssayDetailSerializer,
    EssayGetLinkToFormCreateSerializer,
    EssayFormURLCreateSerializer,
)
from .permissions import (
    OwnUserPermission,
    IsWorkAcceptingStage,
    IsWorkDoesNotAlreadyExists,
    IsFormURLAlreadyExists,
    IsWorkDoesNotAlreadyExistsFromFormURL,
)
from ...models import FormURL


class EssayCreate(generics.CreateAPIView):
    serializer_class = EssayCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsWorkAcceptingStage, IsWorkDoesNotAlreadyExists]


class EssayListView(generics.ListAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayListSerializer
    permission_classes = [permissions.IsAdminUser]


class EssayDetailView(generics.RetrieveUpdateAPIView):
    queryset = Essay.objects.all()
    serializer_class = EssayDetailSerializer
    permission_classes = [OwnUserPermission, IsWorkAcceptingStage]


class EssayGetLinkToFormView(generics.CreateAPIView):
    serializer_class = EssayGetLinkToFormCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFormURLAlreadyExists]


class EssayFormURLCreate(generics.CreateAPIView):
    serializer_class = EssayFormURLCreateSerializer
    permission_classes = [permissions.AllowAny, IsWorkAcceptingStage, IsWorkDoesNotAlreadyExistsFromFormURL]

    def create(self, request, *args, **kwargs):
        form_url = FormURL.get_from_url(url=kwargs['pk'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})
        added_essay = Essay.objects.create(
            task=Text.get_current(),
            body=request.data['body'],
            author=form_url.user
        )
        return Response(EssayFormURLCreateSerializer(added_essay).data, status=status.HTTP_201_CREATED)  # TODO: change EssayFormURLCreateSerializer