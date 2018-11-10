from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin

from sirius_recomendations.views import recommend_achievements

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recommend_achievement', recommend_achievements),
]
