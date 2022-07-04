from rest_framework import serializers
from ..models import Essay, Text
from ...serializers import UserDetailSerializer
from ..texts.serializers import TextDetailSerializer


class EssayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = ['id', 'week_id', 'author', 'body']

    week_id = serializers.SerializerMethodField()

    @staticmethod
    def get_week_id(obj):
        return obj.task.week_id


class EssayDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

    author = UserDetailSerializer(read_only=True)
    task = TextDetailSerializer(read_only=True)


class EssayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

    created_at = serializers.DateTimeField(read_only=True)
    task = TextDetailSerializer(read_only=True)

    def create(self, validated_data):
        current_text = Text.get_current_task()
        return Essay.objects.create(task=current_text, **validated_data)
