from rest_framework import serializers
from ..models import Essay, Text
from ...form_url.models import EssayFormURL
from ...serializers import UserDetailSerializer
from ..texts.serializers import TextDetailSerializer, WeekIDSerializer


class EssayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['id', 'week_id', 'author', 'body']

    week_id = serializers.SerializerMethodField()

    @staticmethod
    def get_week_id(obj):
        return str(obj.task.week_id)


class EssayDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

    author = UserDetailSerializer(read_only=True)
    task = TextDetailSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class EssayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

    created_at = serializers.DateTimeField(read_only=True)
    task = TextDetailSerializer(read_only=True)

    def create(self, validated_data):
        current_text = Text.get_current()
        return Essay.objects.create(task=current_text, **validated_data)


class EssayFormCreateSerializer(serializers.ModelSerializer):
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
        fields = '__all__'

    created_at = serializers.DateTimeField(read_only=True)
    task = TextDetailSerializer(read_only=True)
    author = UserDetailSerializer(read_only=True)


