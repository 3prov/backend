from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

from api.form_url.models import ResultsFormURL
from api.rus.evaluations.models import (
    EssayEvaluation,
    RateEssayEvaluation,
    EssayCriteria,
)
from api.rus.evaluations.serializers import EssayEvaluationDetailSerializer
from api.rus.results.serializers import (
    WeekResultsFormSerializer,
    RateEssayEvaluationSerializer,
)


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


class WeekResultsFormURLUserListView(generics.ListAPIView):
    serializer_class = WeekResultsFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ResultsFormURL.objects.filter(
            user=self.kwargs['user'],
        ).order_by('-week_id__week_number', '-week_id__study_year_from')
        return queryset


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


class RateEssayEvaluationFromFormURLCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RateEssayEvaluationSerializer

    def create(self, request, *args, **kwargs):
        form_url = ResultsFormURL.get_from_url(url=self.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError(
                detail='Ссылка недействительна.'
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        evaluation_criteria = EssayCriteria.objects.get(
            id=serializer.data['evaluation_criteria']
        )
        if form_url.week_id != evaluation_criteria.evaluation.work.task.week_id:
            raise permissions.exceptions.ValidationError(
                detail='Эта оценка не принадлежит этой неделе.'
            )
        if RateEssayEvaluation.objects.filter(
            rater=form_url.user,
            evaluation_criteria_id=serializer.data['evaluation_criteria'],
        ).exists():
            raise permissions.exceptions.ValidationError(
                detail='Вы уже оценили эту проверку.'
            )
        RateEssayEvaluation.objects.create(
            rater=form_url.user,
            evaluation_criteria_id=serializer.data['evaluation_criteria'],
            score=serializer.data['score'],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
