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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']

    read_only = ['id', 'email', 'date_joined', 'username']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'vkontakte_id',
            'telegram_id',
        ]

    required = ['username', 'password', 'vkontakte_id', 'telegram_id']

    def create(self, validated_data):
        """
        Хеширует пароль при создании пользователя.
        """
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
