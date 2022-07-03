from rest_framework import serializers
from .models import Text
from django.conf import settings
import re


class TextListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'teacher', 'author', 'created_at']


class TextDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'

    def validate(self, data):
        if 'week_id' not in data.keys():
            return data
        if len(data['week_id']) != 12:
            raise serializers.ValidationError({'week_id': 'Поле должно содержать 12 символов.'})
        if not bool(re.match(r'^\d{4}-\d{4}_\d{2,3}$', data['week_id'])):
            raise serializers.ValidationError({'week_id': 'Нарушен формат поля. Пример формата: 2022-2023_07, '
                                                          'где 2022 - это начало учебного года, 2023 - конец, '
                                                          '07 - номер недели.'})
        return data


class TextCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'

    week_id = serializers.CharField(read_only=Text)
    created_at = serializers.DateTimeField(read_only=Text)

    def create(self, validated_data):
        previous_text = Text.objects.order_by('-created_at').first()
        if not previous_text:
            return Text.objects.create(week_id=f"{settings.STUDY_YEAR}_00", **validated_data)

        next_week_number = int(previous_text.week_id.split('_')[-1]) + 1
        return Text.objects.create(week_id=f"{settings.STUDY_YEAR}_{next_week_number:02d}", **validated_data)

