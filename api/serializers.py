# -*- coding: utf-8 -*-
from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
)

from api.models import AdminUser, VKUser


class AdminUserSerializer():
    class Meta:
        model = AdminUser
        fields = (
            'user',
            'vk_id', 'vk_token'
        )


class VKUserSerializer(HyperlinkedModelSerializer):
    auth_token = SerializerMethodField()

    def get_auth_token(self, obj):
        return obj.auth_token.hex

    class Meta:
        model = VKUser

        fields = (
            'vk_id', 'vk_token', 'auth_token', 'phone', 'is_phone_confirmed',
            'email', 'is_email_confirmed', 'point', "city"
        )
