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
from ...services import all_objects


class TextCreate(generics.CreateAPIView):
    serializer_class = TextCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class TextListView(generics.ListAPIView):
    queryset = all_objects(
        Text.objects, order_by=('-week_id__week_number', '-week_id__study_year_from')
    )
    serializer_class = TextListSerializer
    permission_classes = [permissions.AllowAny]


class TextDetailView(generics.RetrieveUpdateAPIView):
    queryset = all_objects(Text.objects)
    serializer_class = TextSerializer
    permission_classes = [permissions.IsAdminUser]


class TextKeyCreateView(generics.CreateAPIView):
    serializer_class = TextKeyCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class TextByFormURLView(generics.RetrieveAPIView):
    serializer_class = TextWithKeysSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        form_url = ResultsFormURL.get_from_url_or_404(url=self.kwargs['encoded_part'])
        return form_url.week_id.task


class TextView(generics.RetrieveAPIView):
    queryset = all_objects(Text.objects)
    serializer_class = TextWithKeysSerializer
    permission_classes = [permissions.AllowAny]
