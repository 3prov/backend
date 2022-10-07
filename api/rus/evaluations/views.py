import random

from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.form_url.models import EvaluationFormURL
from api.control.models import WeekID
from api.models import User
from api.rus.evaluations.models import EssayEvaluation, EssaySelectionReview
from api.rus.evaluations.permissions import IsEvaluationAcceptingStage
from api.rus.evaluations.serializers import (
    EvaluationFormURLGetCurrentWeekListSerializer,
    EvaluationFormURLListViewSerializer,
    EssayCriteriaDetailSerializer,
    EssayEvaluationSerializer,
    EvaluationFormURLVolunteerCreateSerializer,
    EssaySelectionReviewSerializer,
    EssaySelectionReviewWithoutSelectionSerializer,
)
from api.rus.models import Essay
from api.services import all_objects, filter_objects, get_object
from api.work_distribution.models import WorkDistributionToEvaluate

from django_filters.rest_framework import DjangoFilterBackend


class EssaySelectionReviewFromFormURLCreate(generics.CreateAPIView):
    queryset = all_objects(EssaySelectionReview.objects)
    serializer_class = EssaySelectionReviewSerializer
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]

    def create(self, request, *args, **kwargs):
        form_url = EvaluationFormURL.get_from_url_or_404(url=kwargs['encoded_part'])
        serialized = self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        if not (
            0
            <= serialized.data['start_selection_char_index']
            < form_url.evaluation_work.chars_count
        ):
            raise permissions.exceptions.ValidationError(
                detail='Индекс начального символа выделения не может быть отрицательным числом.'
            )
        if not (
            0
            <= serialized.data['start_selection_char_index']
            + serialized.data['selection_length']
            <= form_url.evaluation_work.chars_count
        ):
            raise permissions.exceptions.ValidationError(
                detail='Индекс конца выделения должен быть больше 0 и не больше длины текста сочинения.'
            )

        if filter_objects(
            EssaySelectionReview.objects,
            evaluator=form_url.user,
            essay=form_url.evaluation_work,
            start_selection_char_index=serialized.data['start_selection_char_index'],
            selection_length=serialized.data['selection_length'],
        ).exists():
            raise permissions.exceptions.ValidationError(
                {'detail': 'Проверка этого фрагмента уже отправлена.'}
            )

        added_selection_review = EssaySelectionReview.objects.create(
            start_selection_char_index=serialized.data['start_selection_char_index'],
            selection_length=serialized.data['selection_length'],
            evaluator_comment=serialized.data['evaluator_comment'],
            mistake_type=serialized.data['mistake_type'],
            essay=form_url.evaluation_work,
            evaluator=form_url.user,
        )
        return Response(
            self.get_serializer(added_selection_review).data,
            status=status.HTTP_201_CREATED,
        )


class EssaySelectionReviewFormURLView(generics.RetrieveUpdateAPIView):
    queryset = all_objects(EssaySelectionReview.objects)
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]
    serializer_class = EssaySelectionReviewWithoutSelectionSerializer

    def get_object(self):
        form_url = EvaluationFormURL.get_from_url_or_404(
            url=self.kwargs['encoded_part']
        )
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            evaluator=form_url.user,
            essay=form_url.evaluation_work,
            start_selection_char_index=self.kwargs['start_selection_char_index'],
            selection_length=self.kwargs['selection_length'],
        )
        return obj


class EvaluationFormURLGetCurrentWeekList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EvaluationFormURLGetCurrentWeekListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['evaluator', 'work', 'is_required']

    def get_queryset(self):
        return filter_objects(
            WorkDistributionToEvaluate.objects, week_id=WeekID.get_current()
        )


class EvaluationFormURLListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EvaluationFormURLListViewSerializer

    def get_queryset(self):
        return filter_objects(
            EvaluationFormURL.objects,
            week_id=WeekID.get_current(),
            user=self.kwargs['user'],
        )


class EvaluationFormURLWorkCreate(generics.CreateAPIView):
    queryset = all_objects(EvaluationFormURL.objects)
    serializer_class = EssayEvaluationSerializer
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        form_url = EvaluationFormURL.get_from_url_or_404(url=kwargs['encoded_part'])
        if filter_objects(
            EssayEvaluation.objects,
            evaluator=form_url.user,
            work=form_url.evaluation_work,
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
        # filter_objects(
        # EssaySentenceReview.objects,essay=form_url.evaluation_work, evaluator=form_url.user) <--- RETURN IN TOO
        return Response(
            self.get_serializer(added_evaluation).data,
            status=status.HTTP_201_CREATED,
        )  # TODO: change EvaluationFormURLCreateSerializer


class EvaluationFormURLView(generics.RetrieveUpdateAPIView):
    queryset = all_objects(EssayEvaluation.objects)
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
            volunteer = get_object(User.objects, id=_volunteer_uuid)
        except User.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                detail='Пользователь с таким UUID не найден.'
            )

        queryset = filter_objects(
            WorkDistributionToEvaluate.objects,
            evaluator=volunteer,
            week_id=WeekID.get_current(),
        )
        if queryset.exists():
            return queryset
        WorkDistributionToEvaluate.make_optionally_for_volunteer(volunteer)
        return filter_objects(
            WorkDistributionToEvaluate.objects,
            evaluator=volunteer,
            week_id=WeekID.get_current(),
        )


class EvaluationFormURLVolunteerCreate(generics.CreateAPIView):
    queryset = all_objects(EvaluationFormURL.objects)
    serializer_class = EvaluationFormURLVolunteerCreateSerializer
    permission_classes = [permissions.IsAdminUser, IsEvaluationAcceptingStage]

    def create(self, request, *args, **kwargs):
        _volunteer_uuid = self.kwargs['user']
        try:
            volunteer = get_object(User.objects, id=_volunteer_uuid)
        except User.DoesNotExist:
            raise permissions.exceptions.ValidationError(
                detail='Пользователь с таким UUID не найден.'
            )

        # TODO: убрать ORM запросы из views
        current_week_id = WeekID.get_current()
        forms = filter_objects(
            EvaluationFormURL.objects,
            user=volunteer,
            week_id=current_week_id,
        )
        # проверка если количество форм пользователя уже равняется числу сочинений
        # на текущей неделе
        if forms.count() == filter_objects(
            Essay.objects, task__week_id=current_week_id
        ).count() - int(volunteer.is_week_participant):
            return Response(
                EvaluationFormURLListViewSerializer(forms, many=True).data,
                status=status.HTTP_200_OK,
            )

        # проверка чтобы пользователь не смог проверить необязательные работы
        # до проверки обязательных
        if (
            filter_objects(
                EssayEvaluation.objects,
                evaluator=volunteer,
                work__task__week_id=current_week_id,
            ).count()
            < 3
            and volunteer.is_week_participant
        ):
            raise permissions.exceptions.ValidationError(
                detail='Необходимо вначале проверить обязательные работы.'
            )

        work_distribution = filter_objects(
            WorkDistributionToEvaluate.objects,
            evaluator=volunteer,
            week_id=current_week_id,
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
                filter_objects(
                    EvaluationFormURL.objects, user=volunteer, week_id=current_week_id
                ),
                many=True,
            ).data,
            status=status.HTTP_201_CREATED,
        )
