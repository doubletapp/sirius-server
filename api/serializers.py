from collections import defaultdict

from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
)

from api.models import AdminUser, VKUser, Course


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


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'course_template', 'date')


class QuestionSerializer(ModelSerializer):

    educational_trajectory_list = SerializerMethodField()
    educational_feed_list = SerializerMethodField()

    def get_educational_trajectory_list(self, instance):
        data = defaultdict(list)
        a = instance.educational_trajectory.get_queryset()
        for i in a:
            data[i.class_start].append({
                "title": i.title,
                "course_type": i.course_type,
                "regularity": i.regularity,
                "class_start": i.class_start,
                "class_end": i.class_end,
                "intramuraled": i.intramuraled,
                "command": i.command,
                "url": i.url,
                "specialization": i.specialization,
            })

        return data

    def get_educational_feed_list(self, instance):
        data = []
        a = instance.educational_feed.get_queryset()
        for i in a:
            data.append({
                "type": "course",
                "title": i.course_template.title,
                "course_type": i.course_template.course_type,
                "regularity": i.course_template.regularity,
                "class_start": i.course_template.class_start,
                "class_end": i.course_template.class_end,
                "intramuraled": i.course_template.intramuraled,
                "command": i.course_template.command,
                "url": i.course_template.url,
                "specialization": i.course_template.specialization,
                "date": i.date.strftime("%d-%m-%Y"),
            })

        return data

    class Meta:
        model = VKUser
        fields = ('educational_trajectory_list', 'educational_feed_list')