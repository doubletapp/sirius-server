import json

from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from api.models import VKUser, Course
from api.serializers import VKUserSerializer, CourseSerializer, QuestionSerializer


class CustomModelViewSet(ModelViewSet):
    def create(self, request, data, *args, **kwargs):

        # Если существует вк-юзер - его нужно прописать как владельца
        vk_user = getattr(request.user, "vk_user", None)
        if vk_user:
            request.data.update({"author": vk_user.vk_id})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instns = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return instns, Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VKUserViewSet(CustomModelViewSet):
    queryset = VKUser.objects.all()
    serializer_class = VKUserSerializer

    def create(self, request, *args, **kwargs):

        data = request.data
        vk_id = data.get("vk_id")
        sirius_id = data.get("sirius_id")
        if not vk_id and not sirius_id:
            data = json.loads(list(request.data.keys())[0])

        try:

            vk_user = VKUser.objects.get(
                vk_id=data.get("vk_id")
            )
            if getattr(request.user, "vk_user", None):
                data["vk_token"] = vk_user.vk_token

            self.get_object = lambda: vk_user
            return super(VKUserViewSet, self).update(request, *args, **kwargs)

        except VKUser.DoesNotExist:
            try:
                vk_user = VKUser.objects.get(
                    sirius_id=data.get("sirius_id"),
                    sirius_password=data.get("sirius_password"),
                )
                if getattr(request.user, "vk_user", None):
                    data["vk_token"] = vk_user.vk_token

                self.get_object = lambda: vk_user
                return super(VKUserViewSet, self).update(request, *args, **kwargs)
            except VKUser.DoesNotExist:
                pass

            instns, response = super(VKUserViewSet, self).create(request, data, *args, **kwargs)

            return response


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class QuestionViewSet(ModelViewSet):
    queryset = VKUser.objects.all()
    serializer_class = QuestionSerializer