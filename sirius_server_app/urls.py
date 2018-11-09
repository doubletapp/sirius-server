from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin


router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
