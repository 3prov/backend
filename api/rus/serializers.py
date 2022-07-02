from rest_framework import serializers
from .models import Text
from django.conf import settings


class TextListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'teacher', 'author', 'created_at']


class TextDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


class TextCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ['created_at', 'week_id']

    def create(self, validated_data):
        previous_text = Text.objects.order_by('-created_at').first()
        if not previous_text:
            return Text.objects.create(week_id=f"{settings.STUDY_YEAR}_00", **validated_data)

        next_week_number = int(previous_text.week_id.split('_')[-1]) + 1
        return Text.objects.create(week_id=f"{settings.STUDY_YEAR}_{next_week_number:02d}", **validated_data)
