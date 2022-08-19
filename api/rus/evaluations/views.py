import random

from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.form_url.models import EvaluationFormURL
from api.management.models import WeekID
from api.models import User
from api.rus.evaluations.models import EssayEvaluation, EssaySentenceReview
from api.rus.evaluations.permissions import IsEvaluationAcceptingStage
from api.rus.evaluations.serializers import (
    EvaluationFormURLGetCurrentWeekListSerializer,
    EvaluationFormURLListViewSerializer,
    EssayCriteriaDetailSerializer,
    EssayEvaluationSerializer,
    EvaluationFormURLVolunteerCreateSerializer,
    EssaySentenceReviewSerializer,
)
from api.rus.models import Essay
from api.work_distribution.models import WorkDistributionToEvaluate

from django_filters.rest_framework import DjangoFilterBackend


class EssaySentenceReviewFromFormURLCreate(generics.CreateAPIView):
    queryset = EssaySentenceReview.objects.all()
    serializer_class = EssaySentenceReviewSerializer
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]

    def create(self, request, *args, **kwargs):
        form_url = EvaluationFormURL.get_from_url_or_404(url=kwargs['encoded_part'])
        serialized = self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        if not (
            0
            < serialized.data['sentence_number']
            <= form_url.evaluation_work.sentences_count
        ):
            raise permissions.exceptions.ValidationError(
                detail='Номер оцениваемого предложения не может быть больше '
                'количества предложений сочинения.'
            )

        if EssaySentenceReview.objects.filter(
            evaluator=form_url.user,
            essay=form_url.evaluation_work,
            sentence_number=serialized.data['sentence_number'],
        ).exists():
            raise permissions.exceptions.ValidationError(
                {'detail': 'Проверка этого предложения уже отправлена.'}
            )

        added_sentence_review = EssaySentenceReview.objects.create(
            sentence_number=serialized.data['sentence_number'],
            evaluator_comment=serialized.data['evaluator_comment'],
            mistake_type=serialized.data['mistake_type'],
            essay=form_url.evaluation_work,
            evaluator=form_url.user,
        )
        return Response(
            self.get_serializer(added_sentence_review).data,
            status=status.HTTP_201_CREATED,
        )


class EssaySentenceReviewFormURLView(generics.RetrieveUpdateAPIView):
    queryset = EssaySentenceReview.objects.all()
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]
    serializer_class = EssaySentenceReviewSerializer

    def get_object(self):
        form_url = EvaluationFormURL.get_from_url_or_404(
            url=self.kwargs['encoded_part']
        )
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            evaluator=form_url.user,
            essay=form_url.evaluation_work,
            sentence_number=self.kwargs['sentence_number'],
        )
        return obj


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
        return EvaluationFormURL.objects.filter(
            week_id=WeekID.get_current(), user=self.kwargs['user']
        )


class EvaluationFormURLWorkCreate(generics.CreateAPIView):
    queryset = EvaluationFormURL.objects.all()
    serializer_class = EssayEvaluationSerializer
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        form_url = EvaluationFormURL.get_from_url_or_404(url=kwargs['encoded_part'])
        if EssayEvaluation.objects.filter(
            evaluator=form_url.user, work=form_url.evaluation_work
        ).exists():
            raise permissions.exceptions.ValidationError(
                {'detail': 'Проверка уже отправлена.'}
            )

        if 'criteria' not in request.data.keys():
            raise permissions.exceptions.ValidationError(
                detail='Ошибка сериализации модели Критериев.'
            )

        criteria = EssayCriteriaDetailSerializer(data=request.data['criteria'])
        criteria.is_valid(raise_exception=True)
        criteria_instance = criteria.save()
        added_evaluation = EssayEvaluation.objects.create(
            work=form_url.evaluation_work,
            evaluator=form_url.user,
            criteria=criteria_instance,
        )
        # EssaySentenceReview.objects.filter(essay=form_url.evaluation_work, evaluator=form_url.user) <--- RETURN IN TOO
        return Response(
            self.get_serializer(added_evaluation).data,
            status=status.HTTP_201_CREATED,
        )  # TODO: change EvaluationFormURLCreateSerializer


class EvaluationFormURLView(generics.RetrieveUpdateAPIView):
    queryset = EssayEvaluation.objects.all()
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]
    serializer_class = EssayEvaluationSerializer

    def get_object(self):
        form_url = EvaluationFormURL.get_from_url_or_404(
            url=self.kwargs['encoded_part']
        )
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, evaluator=form_url.user, work=form_url.evaluation_work
        )
        return obj


class WorkDistributionToEvaluateVolunteerListView(generics.ListAPIView):
    serializer_class = EvaluationFormURLGetCurrentWeekListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        _volunteer_uuid = self.kwargs['user']
        try:
            volunteer = User.objects.get(id=_volunteer_uuid)
        except User.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                detail='Пользователь с таким UUID не найден.'
            )

        queryset = WorkDistributionToEvaluate.objects.filter(
            evaluator=volunteer, week_id=WeekID.get_current()
        )
        if queryset.exists():
            return queryset
        WorkDistributionToEvaluate.make_optionally_for_volunteer(volunteer)
        return WorkDistributionToEvaluate.objects.filter(
            evaluator=volunteer, week_id=WeekID.get_current()
        )


class EvaluationFormURLVolunteerCreate(generics.CreateAPIView):
    queryset = EvaluationFormURL.objects.all()
    serializer_class = EvaluationFormURLVolunteerCreateSerializer
    permission_classes = [permissions.IsAdminUser, IsEvaluationAcceptingStage]

    def create(self, request, *args, **kwargs):
        _volunteer_uuid = self.kwargs['user']
        try:
            volunteer = User.objects.get(id=_volunteer_uuid)
        except User.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                detail='Пользователь с таким UUID не найден.'
            )

        # TODO: убрать ORM запросы из views
        current_week_id = WeekID.get_current()
        forms = EvaluationFormURL.objects.filter(
            user=volunteer,
            week_id=current_week_id,
        )
        # проверка если количество форм пользователя уже равняется числу сочинений
        # на текущей неделе
        if (
            forms.count()
            == Essay.objects.filter(task__week_id=current_week_id).count() - 1
        ):
            return Response(
                EvaluationFormURLListViewSerializer(forms, many=True).data,
                status=status.HTTP_200_OK,
            )

        # проверка чтобы пользователь не смог проверить необязательные работы
        # до проверки обязательных
        if (
            EssayEvaluation.objects.filter(
                evaluator=volunteer, work__task__week_id=current_week_id
            ).count()
            < 3
            and Essay.objects.filter(
                author=volunteer, task__week_id=current_week_id
            ).exists()
        ):
            raise permissions.exceptions.ValidationError(
                detail='Необходимо вначале проверить обязательные работы.'
            )

        work_distribution = WorkDistributionToEvaluate.objects.filter(
            evaluator=volunteer, week_id=current_week_id
        )
        if not work_distribution.exists():
            raise permissions.exceptions.ValidationError(
                detail='Распределение для пользователя не производилось.'
            )

        work_distribution_essays = set(wd.work for wd in work_distribution)
        form_evaluation_essays = set(f.evaluation_work for f in forms)
        difference = work_distribution_essays.difference(form_evaluation_essays)
        picked_essay = random.choice(list(difference))

        EvaluationFormURL.objects.create(
            user=volunteer, evaluation_work=picked_essay, week_id=current_week_id
        )

        return Response(
            EvaluationFormURLListViewSerializer(
                EvaluationFormURL.objects.filter(
                    user=volunteer, week_id=current_week_id
                ),
                many=True,
            ).data,
            status=status.HTTP_200_OK,
        )
