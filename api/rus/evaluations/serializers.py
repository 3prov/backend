from rest_framework import serializers

from api.form_url.models import EvaluationFormURL
from api.rus.evaluations.models import (
    EssayEvaluation,
    EssaySelectionReview,
    EssayCriteria,
)
from api.work_distribution.models import WorkDistributionToEvaluate


class EvaluationFormURLGetCurrentWeekListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDistributionToEvaluate
        fields = '__all__'

    # work = EssayDetailSerializer(read_only=True)
    # evaluator = UserDetailSerializer(read_only=True)


class EssaySelectionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssaySelectionReview
        fields = [
            'start_selection_char_index',
            'selection_length',
            'evaluator_comment',
            'mistake_type',
        ]


class EssaySelectionReviewWithoutSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssaySelectionReview
        fields = ['evaluator_comment', 'mistake_type']


class EvaluationFormURLListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationFormURL
        fields = '__all__'


class EssayCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayCriteria
        fields = '__all__'


class EssayCriteriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayCriteria
        fields = ['score']


class EssayCriteriaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayCriteria
        fields = '__all__'


class EvaluationFormURLWorkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayEvaluation
        fields = ['criteria', 'created_at']

    criteria = EssayCriteriaSerializer()
    created_at = serializers.DateTimeField(read_only=True)


class EssayEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayEvaluation
        fields = ['criteria', 'created_at', 'selections_review']

    created_at = serializers.DateTimeField(read_only=True)
    criteria = EssayCriteriaSerializer()
    selections_review = serializers.SerializerMethodField(read_only=True)

    def update(self, instance, validated_data):
        EssayCriteria.objects.filter(evaluation=instance).update(
            **validated_data['criteria']
        )
        return instance

    @staticmethod
    def get_selections_review(obj):
        essay_selections_review = EssaySelectionReview.objects.filter(
            evaluator=obj.evaluator, essay=obj.work
        )
        return EssaySelectionReviewSerializer(essay_selections_review, many=True).data


class EssayEvaluationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayEvaluation
        fields = ['criteria_score']

    criteria_score = serializers.SerializerMethodField()

    @staticmethod
    def get_criteria_score(obj):
        return obj.criteria.score


class EvaluationFormURLVolunteerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationFormURL
        fields = '__all__'

    url = serializers.URLField(read_only=True)
    week_id = serializers.URLField(read_only=True)
    evaluation_work = EssayEvaluationSerializer(read_only=True)
