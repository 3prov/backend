from rest_framework import serializers

from ..evaluations.serializers import (
    EssayEvaluationSerializer,
    EssayEvaluationListSerializer,
)
from ..models import Essay, Text
from ...form_url.models import EssayFormURL
from ...serializers import UserActiveSerializer
from ..texts.serializers import (
    TextDetailSerializer,
    WeekIDSerializer,
    TextWithKeysSerializer,
)


class EssayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['id', 'week_id', 'body', 'evaluations']

    week_id = serializers.SerializerMethodField(read_only=True)
    evaluations = EssayEvaluationListSerializer(read_only=True, many=True)

    @staticmethod
    def get_week_id(obj):
        return str(obj.task.week_id)


class EssayDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

    author = UserActiveSerializer(read_only=True)
    task = TextDetailSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['body', 'created_at']


class EssayWithEvaluationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['body', 'created_at', 'task', 'evaluations']

    task = TextWithKeysSerializer(read_only=True)
    evaluations = EssayEvaluationSerializer(read_only=True, many=True)


class EssayFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayFormURL
        fields = '__all__'

    url = serializers.SerializerMethodField(read_only=True)  # TODO: URLField
    week_id = WeekIDSerializer(read_only=True)

    @staticmethod
    def get_url(obj):
        return obj.url

    @staticmethod
    def get_week_id(obj):
        return obj.week_id


class EssayFormURLCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['created_at', 'body']

    created_at = serializers.DateTimeField(read_only=True)
