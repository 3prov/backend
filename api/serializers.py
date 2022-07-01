from rest_framework import serializers
from .models import User, AuthSocialID
from django.db import transaction


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'social_network']


class AuthSocialIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthSocialID
        exclude = ['id']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']

    social_network = AuthSocialIDSerializer()
    read_only = ['id', 'email', 'date_joined', 'username']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'social_network']

    social_network = AuthSocialIDSerializer()

    required = ['username', 'password', 'social_network']

    @transaction.atomic
    def create(self, validated_data):
        auth_social_id = AuthSocialID.objects.create(
            vkontakte=validated_data['social_network'].get('vkontakte', None),
            telegram=validated_data['social_network'].get('telegram', None)
        )
        del validated_data['social_network']
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.social_network = auth_social_id
        user.save()
        return user
