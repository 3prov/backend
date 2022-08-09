from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.form_url.models import ResultsFormURL
from api.rus.evaluations.models import EssayEvaluation
from api.rus.evaluations.serializers import EssayEvaluationDetailSerializer
from api.rus.results.permissions import IsWeekResultsFormURLAlreadyExists
from api.rus.results.serializers import WeekResultsFormCreateSerializer


class WeekResultsListView(generics.ListAPIView):
    queryset = EssayEvaluation.objects.all()
    serializer_class = EssayEvaluationDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'work__task__week_id',  # TODO: `task__week_id` is id
        'evaluator__username',
        'evaluator__id',
        'work__author__username',
        'work__author__id',  # TODO: проверить, если автор отправляет работы на разных неделях, то результат отображается для всех недель?
    ]


class WeekResultsFormURLUserCreate(generics.CreateAPIView):
    serializer_class = WeekResultsFormCreateSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsWeekResultsFormURLAlreadyExists,
    ]


class WeekResultsFromFormURLListView(generics.ListAPIView):
    queryset = EssayEvaluation.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EssayEvaluationDetailSerializer

    def list(self, request, *args, **kwargs):
        form_url = ResultsFormURL.get_from_url(url=self.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError(
                {'detail': 'Ссылка недействительна.'}
            )
        queryset = self.get_queryset()
        obj = queryset.filter(
            work__author=form_url.user, work__task__week_id=form_url.week_id
        )
        return Response(EssayEvaluationDetailSerializer(obj, many=True).data)
