from django.contrib.admin import site, ModelAdmin
from api.models import VKUser, AdminUser, Course, CourseTemplate


class VKUserAdmin(ModelAdmin):
    pass


class CourseAdmin(ModelAdmin):
    pass


class CourseTemplateAdmin(ModelAdmin):
    list_filter = ('source',)


site.register(VKUser, VKUserAdmin)
site.register(Course, CourseAdmin)
site.register(CourseTemplate, CourseTemplateAdmin)