from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.form_url.models import EvaluationFormURL
from api.management.models import WeekID
from api.rus.evaluations.models import EssayEvaluation, EssaySentenceReview
from api.rus.evaluations.permissions import IsEvaluationAcceptingStage
from api.rus.evaluations.serializers import EvaluationFormURLGetCurrentWeekListSerializer, \
    EssaySentenceReviewCreateSerializer, EvaluationFormURLListViewSerializer, EvaluationFormURLCreateSerializer, \
    EssayCriteriaDetailSerializer, EssayEvaluationDetailSerializer
from api.work_distribution.models import WorkDistributionToEvaluate

from django_filters.rest_framework import DjangoFilterBackend


class EssaySentenceReviewCreate(generics.CreateAPIView):

    serializer_class = EssaySentenceReviewCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class EvaluationFormURLGetCurrentWeekList(generics.ListAPIView):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = EvaluationFormURLGetCurrentWeekListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evaluator', 'work', 'is_required']

    def get_queryset(self):
        return WorkDistributionToEvaluate.objects.filter(week_id=WeekID.get_current())


class EvaluationFormURLListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EvaluationFormURLListViewSerializer

    def get_queryset(self):
        return EvaluationFormURL.objects.filter(week_id=WeekID.get_current(), user=self.kwargs['user'])


#class EvaluationFormURLGetUserLink(generics.ListAPIView):


class EvaluationFormURLCreate(generics.CreateAPIView):
    queryset = EvaluationFormURL.objects.all()
    serializer_class = EvaluationFormURLCreateSerializer
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        form_url = EvaluationFormURL.get_from_url(url=kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})

        if EssayEvaluation.objects.filter(evaluator=form_url.user, work=form_url.evaluation_work).exists():
            raise permissions.exceptions.ValidationError({'detail': 'Проверка уже отправлена.'})

        if 'criteria' not in request.data.keys():
            raise permissions.exceptions.ValidationError(detail='Ошибка сериализации модели Критериев.')

        criteria = EssayCriteriaDetailSerializer(data=request.data['criteria'])
        if not criteria.is_valid():
            raise permissions.exceptions.ValidationError(detail='Ошибка сериализации модели Критериев.')
        criteria_instance = criteria.save()
        added_evaluation = EssayEvaluation.objects.create(
            work=form_url.evaluation_work,
            evaluator=form_url.user,
            criteria=criteria_instance
        )
        # EssaySentenceReview.objects.filter(essay=form_url.evaluation_work, evaluator=form_url.user) <--- RETURN IN TOO
        return Response(EvaluationFormURLCreateSerializer(added_evaluation).data, status=status.HTTP_201_CREATED)  # TODO: change EvaluationFormURLCreateSerializer


class EvaluationFormURLView(generics.RetrieveUpdateAPIView):
    queryset = EssayEvaluation.objects.all()
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]
    serializer_class = EssayEvaluationDetailSerializer

    def get_object(self):
        form_url = EvaluationFormURL.get_from_url(url=self.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, evaluator=form_url.user, work=form_url.evaluation_work)
        return obj


