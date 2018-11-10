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
            'vk_id', 'vk_token', 'sirius_id', 'sirius_password', 'auth_token', 'city'
        )
