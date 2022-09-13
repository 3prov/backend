from rest_framework import serializers
from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'vkontakte_id',
            'telegram_id',
        ]


class UserActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_active']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'vkontakte_id',
            'telegram_id',
            'server_uuid',
        ]

    server_uuid = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_server_uuid(obj):
        return obj.id

    def create(self, validated_data):
        """
        Устанавливает `set_unusable_password` на пользователя.
        """
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_unusable_password()
        user.save()
        return user
