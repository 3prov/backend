from rest_framework import serializers, exceptions

from api.form_url.models import EvaluationFormURL
from api.rus.essays.serializers import EssayDetailSerializer
from api.rus.evaluations.models import (
    EssayEvaluation,
    EssaySentenceReview,
    EssayCriteria,
)
from api.serializers import UserDetailSerializer
from api.work_distribution.models import WorkDistributionToEvaluate


class EvaluationFormURLGetCurrentWeekListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDistributionToEvaluate
        fields = '__all__'

    # work = EssayDetailSerializer(read_only=True)
    # evaluator = UserDetailSerializer(read_only=True)


class EssaySentenceReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssaySentenceReview
        fields = '__all__'

    essay = EssayDetailSerializer(read_only=True)
    evaluator = UserDetailSerializer(read_only=True)


class EvaluationFormURLListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationFormURL
        fields = '__all__'


class EssayCriteriaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayCriteria
        fields = '__all__'


class EvaluationFormURLCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayEvaluation
        fields = '__all__'

    criteria = EssayCriteriaDetailSerializer()

    created_at = serializers.DateTimeField(read_only=True)
    work = EssayDetailSerializer(read_only=True)
    evaluator = UserDetailSerializer(read_only=True)


class EssayEvaluationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayEvaluation
        fields = '__all__'

    id = serializers.UUIDField(read_only=True)
    work = EssayDetailSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    evaluator = UserDetailSerializer(read_only=True)
    criteria = EssayCriteriaDetailSerializer()

    def update(self, instance, validated_data):
        EssayCriteria.objects.filter(evaluation=instance).update(
            **validated_data['criteria']
        )
        return instance
