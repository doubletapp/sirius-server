import uuid

from django.utils import timezone
from django.db.models import (
    CharField, IntegerField, TextField, ForeignKey, Model, CASCADE, DateTimeField,
    BooleanField, UUIDField, AutoField, ImageField, OneToOneField, FloatField, URLField, ManyToManyField
)
from django.contrib.auth.models import User as DjangoUser
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField


class AdminUser(Model):
    user = OneToOneField(DjangoUser, on_delete=CASCADE, primary_key=True)
    vk_id = CharField(max_length=100)
    vk_token = CharField(max_length=400)

    def __str__(self):
        return str(self.vk_id)


class CourseTemplate(Model):
    title = CharField(max_length=400)
    course_type = CharField(
        max_length=200,
        choices=(
            ('club', 'club'),
            ('competition', 'competition'),
            ('activity', 'activity'),
            ('unknown', 'unknown'),
        )
    )
    regularity = CharField(max_length=400, blank=True, null=True)
    class_start = IntegerField(default=5)
    class_end = IntegerField(default=11)
    intramuraled = CharField(
        max_length=200,
        choices=(
            ('intramural', 'intramural'),
            ('extramural', 'extramural'),
            ('online', 'online'),
            ('unknown', 'unknown'),
        )
    )
    command = CharField(
        max_length=200,
        choices=(
            ('command', 'command'),
            ('personal', 'personal'),
            ('unknown', 'unknown'),
        )
    )
    url = URLField()
    specialization = CharField(
        max_length=200,
        choices=(
            ('math', 'math'),
            ('history', 'history'),
            ('programming', 'programming'),
            ('unknown', 'unknown'),
        )
    )
    source = CharField(
        max_length=200,
        default='admin',
        choices=(
            ('admin', 'admin'),
            ('sirius', 'sirius'),
        )
    )

    def __str__(self):
        return self.title


class Course(Model):
    course_template = ForeignKey(CourseTemplate, on_delete=True, null=True)
    date = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course_template.title + " " + self.date.strftime("%d-%m-%Y")


class VKUser(Model):
    vk_id = IntegerField(blank=True, null=True)
    vk_token = CharField(max_length=400, blank=True, null=True)
    sirius_id = IntegerField(blank=True, null=True)
    sirius_password = CharField(max_length=100, blank=True, null=True)
    auth_token = UUIDField(default=uuid.uuid4, editable=True)
    create_datetime = DateTimeField(auto_now_add=True)

    city = CharField(max_length=400, null=True, blank=True, default=None)
    current_class = IntegerField(default=5)

    educational_trajectory = ManyToManyField(CourseTemplate, related_name='educational_trajectory_courses', null=True, blank=True,)
    educational_feed = ManyToManyField(Course, related_name='educational_feed_courses', null=True, blank=True,)

    # educational_trajectory = ArrayField(ForeignKey(CourseTemplate, on_delete=True, null=True), size=50)
    # educational_feed = ArrayField(ForeignKey(Course, on_delete=True, null=True), size=100)

    def __str__(self):
        return str(self.vk_id)


REGIONS = ('Адыгея Респ', 'Алтай Респ', 'Алтайский край', 'Амурская обл', 'Архангельская обл', 'Астраханская обл', 'Башкортостан Респ', 'Белгородская обл', 'Брянская обл', 'Бурятия Респ', 'Владимирская обл', 'Волгоградская обл', 'Вологодская обл', 'Воронежская обл', 'Дагестан Респ', 'Еврейская Аобл', 'Забайкальский край', 'Ивановская обл', 'Ингушетия Респ', 'Иркутская обл', 'Кабардино-Балкарская Респ', 'Калининградская обл', 'Калмыкия Респ', 'Калужская обл', 'Камчатский край', 'Карачаево-Черкесская Респ', 'Карелия Респ', 'Кемеровская обл', 'Кировская обл', 'Коми Респ', 'Костромская обл', 'Краснодарский край', 'Красноярский край', 'Курганская обл', 'Курская обл', 'Ленинградская обл', 'Липецкая обл', 'Магаданская обл', 'Марий Эл Респ', 'Мордовия Респ', 'Москва г', 'Московская обл', 'Мурманская обл', 'Ненецкий АО', 'Нижегородская обл', 'Новгородская обл', 'Новосибирская обл', 'Омская обл', 'Оренбургская обл', 'Орловская обл', 'Пензенская обл', 'Пермский край', 'Приморский край', 'Псковская обл', 'Ростовская обл', 'Рязанская обл', 'Самарская обл', 'Санкт-Петербург г', 'Саратовская обл', 'Саха /Якутия/ Респ', 'Сахалинская обл', 'Свердловская обл', 'Северная Осетия - Алания Респ', 'Смоленская обл', 'Ставропольский край', 'Тамбовская обл', 'Татарстан Респ', 'Тверская обл', 'Томская обл', 'Тульская обл', 'Тыва Респ', 'Тюменская обл', 'Удмуртская Респ', 'Ульяновская обл', 'Хабаровский край', 'Хакасия Респ', 'Ханты-Мансийский Автономный округ - Югра АО', 'Челябинская обл', 'Чеченская Респ', 'Чувашская Респ', 'Чукотский АО', 'Ямало-Ненецкий АО', 'Ярославская обл')
