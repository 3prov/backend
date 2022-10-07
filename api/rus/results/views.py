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
from api.rus.essays.serializers import EssayListSerializer
from api.rus.evaluations.serializers import EssayEvaluationSerializer
from api.rus.models import Essay
from api.rus.results.serializers import (
    WeekResultsFormSerializer,
    RateEssayEvaluationSerializer,
    RateEssayEvaluationAnonSerializer,
)
from api.services import all_objects, filter_objects, get_object


class WeekResultsListView(generics.ListAPIView):
    queryset = all_objects(
        Essay.objects,
        order_by=('-task__week_id__week_number', '-task__week_id__study_year_from'),
    )
    serializer_class = EssayListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'task__week_id__week_number',
        'task__week_id__study_year_from',
    ]


class WeekResultsFormURLUserListView(generics.ListAPIView):
    serializer_class = WeekResultsFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = filter_objects(
            ResultsFormURL.objects,
            user=self.kwargs['user'],
            order_by=('-week_id__week_number', '-week_id__study_year_from'),
        )
        return queryset


class WeekResultsFromFormURLListView(generics.ListAPIView):
    queryset = all_objects(EssayEvaluation.objects)
    permission_classes = [permissions.AllowAny]
    serializer_class = EssayEvaluationSerializer

    def list(self, request, *args, **kwargs):
        form_url = ResultsFormURL.get_from_url_or_404(url=self.kwargs['encoded_part'])
        queryset = self.get_queryset()
        obj = queryset.filter(
            work__author=form_url.user, work__task__week_id=form_url.week_id
        )
        return Response(self.get_serializer(obj, many=True).data)


class RateEssayEvaluationFromFormURLCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RateEssayEvaluationSerializer

    def create(self, request, *args, **kwargs):
        form_url = ResultsFormURL.get_from_url_or_404(url=self.kwargs['encoded_part'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        evaluation_criteria = get_object(
            EssayCriteria.objects, id=serializer.data['evaluation_criteria']
        )
        if form_url.week_id != evaluation_criteria.evaluation.work.task.week_id:
            raise permissions.exceptions.ValidationError(
                detail='Эта оценка не принадлежит этой неделе.'
            )
        if filter_objects(
            RateEssayEvaluation.objects,
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


class RateGetByEssayCriteriaView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RateEssayEvaluationAnonSerializer

    def get_object(self):
        obj = EssayCriteria.objects.only('rate').get(
            id=self.kwargs['evaluation_criteria']
        )
        if not hasattr(obj, 'rate'):
            raise permissions.exceptions.ValidationError(
                detail='Автор сочинения ещё не оценил проверку.'
            )
        return obj.rate
