# -*- coding: utf-8 -*-
import uuid
from django.db.models import (
    CharField, IntegerField, TextField, ForeignKey, Model, CASCADE, DateTimeField,
    BooleanField, UUIDField, AutoField, ImageField, OneToOneField, FloatField
)
from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.contrib.gis.db.models import PointField


class AdminUser(Model):
    user = OneToOneField(DjangoUser, on_delete=CASCADE, primary_key=True)
    vk_id = CharField(max_length=100)
    vk_token = CharField(max_length=400)

    def __str__(self):
        return str(self.vk_id)


class VKUser(Model):
    vk_id = CharField(max_length=100, primary_key=True, unique=True)
    vk_token = CharField(max_length=400)
    sirius_id = IntegerField(blank=True, null=True)
    sirius_password = CharField(max_length=100, blank=True, null=True)
    auth_token = UUIDField(default=uuid.uuid4, editable=True)
    create_datetime = DateTimeField(auto_now_add=True)

    city = CharField(max_length=400, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.vk_id)


class Course(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


REGIONS = ('Адыгея Респ', 'Алтай Респ', 'Алтайский край', 'Амурская обл', 'Архангельская обл', 'Астраханская обл', 'Башкортостан Респ', 'Белгородская обл', 'Брянская обл', 'Бурятия Респ', 'Владимирская обл', 'Волгоградская обл', 'Вологодская обл', 'Воронежская обл', 'Дагестан Респ', 'Еврейская Аобл', 'Забайкальский край', 'Ивановская обл', 'Ингушетия Респ', 'Иркутская обл', 'Кабардино-Балкарская Респ', 'Калининградская обл', 'Калмыкия Респ', 'Калужская обл', 'Камчатский край', 'Карачаево-Черкесская Респ', 'Карелия Респ', 'Кемеровская обл', 'Кировская обл', 'Коми Респ', 'Костромская обл', 'Краснодарский край', 'Красноярский край', 'Курганская обл', 'Курская обл', 'Ленинградская обл', 'Липецкая обл', 'Магаданская обл', 'Марий Эл Респ', 'Мордовия Респ', 'Москва г', 'Московская обл', 'Мурманская обл', 'Ненецкий АО', 'Нижегородская обл', 'Новгородская обл', 'Новосибирская обл', 'Омская обл', 'Оренбургская обл', 'Орловская обл', 'Пензенская обл', 'Пермский край', 'Приморский край', 'Псковская обл', 'Ростовская обл', 'Рязанская обл', 'Самарская обл', 'Санкт-Петербург г', 'Саратовская обл', 'Саха /Якутия/ Респ', 'Сахалинская обл', 'Свердловская обл', 'Северная Осетия - Алания Респ', 'Смоленская обл', 'Ставропольский край', 'Тамбовская обл', 'Татарстан Респ', 'Тверская обл', 'Томская обл', 'Тульская обл', 'Тыва Респ', 'Тюменская обл', 'Удмуртская Респ', 'Ульяновская обл', 'Хабаровский край', 'Хакасия Респ', 'Ханты-Мансийский Автономный округ - Югра АО', 'Челябинская обл', 'Чеченская Респ', 'Чувашская Респ', 'Чукотский АО', 'Ямало-Ненецкий АО', 'Ярославская обл')
