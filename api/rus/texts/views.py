from rest_framework import generics, permissions

from ..models import Text
from .serializers import (
    TextCreateSerializer,
    TextListSerializer,
    TextSerializer,
    TextWithKeysSerializer,
    TextKeyCreateSerializer,
)
from ...form_url.models import ResultsFormURL


class TextCreate(generics.CreateAPIView):
    serializer_class = TextCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class TextListView(generics.ListAPIView):
    queryset = Text.objects.all().order_by(
        '-week_id__week_number', '-week_id__study_year_from'
    )
    serializer_class = TextListSerializer
    permission_classes = [permissions.AllowAny]


class TextDetailView(generics.RetrieveUpdateAPIView):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    permission_classes = [permissions.IsAdminUser]


class TextKeyCreateView(generics.CreateAPIView):
    serializer_class = TextKeyCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class TextByFormURLView(generics.RetrieveAPIView):
    serializer_class = TextWithKeysSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        form_url = ResultsFormURL.get_from_url(url=self.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError(
                detail='Ссылка недействительна.'
            )
        return form_url.week_id.task


class TextView(generics.RetrieveAPIView):
    queryset = Text.objects.all()
    serializer_class = TextWithKeysSerializer
    permission_classes = [permissions.AllowAny]
