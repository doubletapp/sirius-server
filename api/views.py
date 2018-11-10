from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.contrib.gis.geos import Point

from api.models import VKUser
from api.serializers import VKUserSerializer


class CustomModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):

        # Если существует вк-юзер - его нужно прописать как владельца
        vk_user = getattr(request.user, "vk_user", None)
        if vk_user:
            request.data.update({"author": vk_user.vk_id})

        # Если существует точка - её нужно преобразовать в исходные тип данных
        if request.data.get("point"):
            point = Point(
                request.data["point"][0],
                request.data["point"][1]
            )
            request.data.update({"point": point})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instns = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return instns, Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VKUserViewSet(CustomModelViewSet):
    queryset = VKUser.objects.all()
    serializer_class = VKUserSerializer

    def create(self, request, *args, **kwargs):

        try:
            vk_user = VKUser.objects.get(
                vk_id=request.data.get("vk_id")
            )

            if getattr(request.user, "vk_user", None):
                request.data["vk_token"] = vk_user.vk_token

            self.get_object = lambda: vk_user
            return super(VKUserViewSet, self).update(request, *args, **kwargs)

        except VKUser.DoesNotExist:
            instns, response = super(VKUserViewSet, self).create(request, *args, **kwargs)

            return response
