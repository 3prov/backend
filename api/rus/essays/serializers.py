from rest_framework import serializers
from ..models import Essay, Text
from ...serializers import UserDetailSerializer
from ..texts.serializers import TextDetailSerializer
from api.management.models import Stage


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

    def validate(self, data):
        if Stage.get_stage() != Stage.StagesEnum.WORK_ACCEPTING:
            raise serializers.ValidationError({
                'detail': f'Ошибка текущего этапа. Для отправки сочинения необходим '
                          f'"{Stage.StagesEnum.WORK_ACCEPTING}", а сейчас "{Stage.get_stage()}" этап'})
        return data


class EssayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

    created_at = serializers.DateTimeField(read_only=True)
    task = TextDetailSerializer(read_only=True)

    def validate(self, data):
        current_text = Text.objects.order_by('-created_at').first()
        already_sent_essay = Essay.objects.filter(author=data['author'], task=current_text)
        if already_sent_essay.exists():
            raise serializers.ValidationError({
                'Сочинение на этой неделе уже существует.': {
                    'id': already_sent_essay.first().id
                }
            })
        if Stage.get_stage() != Stage.StagesEnum.WORK_ACCEPTING:
            raise serializers.ValidationError({
                'detail': f'Ошибка текущего этапа. Для отправки сочинения необходим '
                          f'"{Stage.StagesEnum.WORK_ACCEPTING}", а сейчас "{Stage.get_stage()}" этап'})
        return data

    def create(self, validated_data):
        current_text = Text.objects.order_by('-created_at').first()
        return Essay.objects.create(task=current_text, **validated_data)
