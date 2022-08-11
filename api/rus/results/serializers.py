from rest_framework import serializers

from api.form_url.models import ResultsFormURL
from api.rus.evaluations.models import RateEssayEvaluation
from api.rus.texts.serializers import WeekIDSerializer
from api.serializers import UserDetailSerializer


class WeekResultsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultsFormURL
        fields = '__all__'

    url = serializers.SerializerMethodField(read_only=True)  # TODO: URLField
    week_id = WeekIDSerializer(read_only=True)

    @staticmethod
    def get_url(obj):
        return obj.url


class RateEssayEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateEssayEvaluation
        fields = '__all__'

    rater = UserDetailSerializer(read_only=True)


class RateEssayEvaluationAnonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateEssayEvaluation
        exclude = ['id', 'rater']
