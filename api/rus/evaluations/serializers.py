from rest_framework import serializers

from api.form_url.models import EvaluationFormURL
from api.rus.evaluations.models import (
    EssayEvaluation,
    EssaySentenceReview,
    EssayCriteria,
)
from api.work_distribution.models import WorkDistributionToEvaluate


class EvaluationFormURLGetCurrentWeekListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDistributionToEvaluate
        fields = '__all__'

    # work = EssayDetailSerializer(read_only=True)
    # evaluator = UserDetailSerializer(read_only=True)


class EssaySentenceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssaySentenceReview
        fields = ['sentence_number', 'evaluator_comment', 'mistake_type']


class EssaySentenceReviewWithoutSentenceNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssaySentenceReview
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
        fields = ['criteria', 'created_at', 'sentences_review']

    created_at = serializers.DateTimeField(read_only=True)
    criteria = EssayCriteriaSerializer()
    sentences_review = serializers.SerializerMethodField(read_only=True)

    def update(self, instance, validated_data):
        EssayCriteria.objects.filter(evaluation=instance).update(
            **validated_data['criteria']
        )
        return instance

    @staticmethod
    def get_sentences_review(obj):
        essay_sentences_review = EssaySentenceReview.objects.filter(
            evaluator=obj.evaluator, essay=obj.work
        )
        return EssaySentenceReviewSerializer(essay_sentences_review, many=True).data


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
