from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin

from api.views import VKUserViewSet, CourseViewSet
from sirius_recomendations.views import recommend_achievements

router = routers.DefaultRouter()
router.register(r'auth', VKUserViewSet)
router.register(r'course', CourseViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^recommend_achievement', recommend_achievements),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
