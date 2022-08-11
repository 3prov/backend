from rest_framework import serializers
from ..models import Text, TextKey
from ...management.models import WeekID


class WeekIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekID
        exclude = ['id', 'created_at']


class TextListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['week_id', 'author']

    week_id = WeekIDSerializer()


class TextDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'

    keys = serializers.SerializerMethodField(read_only=True)
    week_id = WeekIDSerializer(read_only=True)

    @staticmethod
    def get_keys(obj):
        text_keys = TextKey.objects.filter(text=obj)
        serializer = TextKeySerializer(text_keys, many=True)
        return serializer.data


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['week_id', 'body', 'author', 'author_description']

    week_id = WeekIDSerializer(read_only=True)


class TextKeyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextKey
        fields = '__all__'


class TextKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = TextKey
        fields = ['range_of_problems', 'authors_position']


class TextWithKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['week_id', 'body', 'author', 'author_description', 'keys']

    week_id = WeekIDSerializer(read_only=True)
    keys = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_keys(obj):
        text_keys = TextKey.objects.filter(text=obj)
        serializer = TextKeySerializer(text_keys, many=True)
        return serializer.data


class TextCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'

    week_id = WeekIDSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
