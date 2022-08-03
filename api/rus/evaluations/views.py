from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.form_url.models import EvaluationFormURL
from api.management.models import WeekID
from api.models import User
from api.rus.evaluations.models import EssayEvaluation, EssaySentenceReview
from api.rus.evaluations.permissions import IsEvaluationAcceptingStage
from api.rus.evaluations.serializers import EvaluationFormURLGetCurrentWeekListSerializer, \
    EssaySentenceReviewCreateSerializer, EvaluationFormURLListViewSerializer, EvaluationFormURLCreateSerializer, \
    EssayCriteriaDetailSerializer, EssayEvaluationDetailSerializer
from api.work_distribution.models import WorkDistributionToEvaluate

from django_filters.rest_framework import DjangoFilterBackend


class EssaySentenceReviewFromFormURLCreate(generics.CreateAPIView):
    queryset = EssaySentenceReview.objects.all()
    serializer_class = EssaySentenceReviewCreateSerializer
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]

    def create(self, request, *args, **kwargs):
        form_url = EvaluationFormURL.get_from_url(url=kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})

        if not EssaySentenceReviewCreateSerializer(data=request.data).is_valid():
            raise permissions.exceptions.ValidationError(detail='Ошибка сериализации модели проверки предложений.')

        if 0 > request.data['sentence_number'] > form_url.evaluation_work.sentences_count:
            raise permissions.exceptions.ValidationError(detail='Номер оцениваемого предложения не может быть больше '
                                                                'количества предложений сочинения.')

        if EssaySentenceReview.objects.filter(
            evaluator=form_url.user,
            essay=form_url.evaluation_work,
            sentence_number=request.data['sentence_number']
        ).exists():
            raise permissions.exceptions.ValidationError({'detail': 'Проверка этого предложения уже отправлена.'})

        added_sentence_review = EssaySentenceReview.objects.create(
            sentence_number=request.data['sentence_number'],
            evaluator_comment=request.data['evaluator_comment'],
            mistake_type=request.data['mistake_type'],
            essay=form_url.evaluation_work,
            evaluator=form_url.user
        )
        return Response(
            EssaySentenceReviewCreateSerializer(added_sentence_review).data,
            status=status.HTTP_201_CREATED
        )


class EssaySentenceReviewFormURLView(generics.RetrieveUpdateAPIView):
    queryset = EssaySentenceReview.objects.all()
    permission_classes = [permissions.AllowAny, IsEvaluationAcceptingStage]
    serializer_class = EssaySentenceReviewCreateSerializer

    def get_object(self):
        form_url = EvaluationFormURL.get_from_url(url=self.kwargs['encoded_part'])
        if not form_url:
            raise permissions.exceptions.ValidationError({'detail': 'Ссылка недействительна.'})
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            evaluator=form_url.user,
            essay=form_url.evaluation_work,
            sentence_number=self.kwargs['sentence_number']
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


class WorkDistributionToEvaluateVolunteerListView(generics.ListAPIView):
    serializer_class = EvaluationFormURLGetCurrentWeekListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        volunteer_uuid = self.kwargs['user']
        try:
            volunteer = User.objects.get(id=volunteer_uuid)
        except User.DoesNotExist:
            raise permissions.exceptions.ValidationError(detail='Пользователь с таким UUID не найден.')

        if WorkDistributionToEvaluate.objects.filter(evaluator=volunteer, week_id=WeekID.get_current()).exists():
            raise permissions.exceptions.PermissionDenied(detail='Распределение для пользователя уже произведено.')
        WorkDistributionToEvaluate.make_optionally_for_volunteer(volunteer)
        return WorkDistributionToEvaluate.objects.filter(evaluator=volunteer, week_id=WeekID.get_current())

