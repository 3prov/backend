from rest_framework import serializers

from api.form_url.models import ResultsFormURL
from api.rus.texts.serializers import WeekIDSerializer


class WeekResultsFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultsFormURL
        fields = '__all__'

    url = serializers.SerializerMethodField(read_only=True)  # TODO: URLField
    week_id = WeekIDSerializer(read_only=True)

    @staticmethod
    def get_url(obj):
        return obj.url

    @staticmethod
    def get_week_id(obj):
        return obj.week_id
