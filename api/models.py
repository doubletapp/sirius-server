import uuid

from django.utils import timezone
from django.db.models import (
    CharField, IntegerField, TextField, ForeignKey, Model, CASCADE, DateTimeField,
    BooleanField, UUIDField, AutoField, ImageField, OneToOneField, FloatField, URLField, ManyToManyField
)
from django.contrib.auth.models import User as DjangoUser
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField


from sirius_recomendations.interest_classifier import predict_proba


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

    math_possibility = FloatField(blank=True, null=True)
    prog_possibility = FloatField(blank=True, null=True)
    hist_possibility = FloatField(blank=True, null=True)
    # educational_trajectory = ArrayField(ForeignKey(CourseTemplate, on_delete=True, null=True), size=50)
    # educational_feed = ArrayField(ForeignKey(Course, on_delete=True, null=True), size=100)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super(VKUser, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
        for tr in self.get_user_recomendations():
            self.educational_trajectory.add(tr)
        self.fill_vk_interests()
        super(VKUser, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def fill_vk_interests(self):
        if not self.vk_id or not self.vk_token:
            return
        try:
            probs = predict_proba(self.vk_id, self.vk_token)
            self.prog_possibility = probs['proger']
            self.math_possibility = probs['math']
            self.hist_possibility = probs['history']

        except:
            pass

    def get_user_recomendations(self):
        if not self.sirius_id:
            return
        import os
        import subprocess
        import json
        dir_path = os.path.dirname(__file__)
        try:
            r = subprocess.Popen(
                "python2 %s %s %s" % (
                    os.path.join(dir_path, '..', 'sirius_recomendations', 'recomendator.py'), self.sirius_id, '[]'
                ),
                shell=True, stdout=subprocess.PIPE).stdout.read()

            for title in json.loads(r.decode('utf-8')):
                try:
                    yield CourseTemplate.objects.get(title=title[:200])
                except:
                    pass
        except:
            return

    def __str__(self):
        return str(self.vk_id)


REGIONS = ('Адыгея Респ', 'Алтай Респ', 'Алтайский край', 'Амурская обл', 'Архангельская обл', 'Астраханская обл', 'Башкортостан Респ', 'Белгородская обл', 'Брянская обл', 'Бурятия Респ', 'Владимирская обл', 'Волгоградская обл', 'Вологодская обл', 'Воронежская обл', 'Дагестан Респ', 'Еврейская Аобл', 'Забайкальский край', 'Ивановская обл', 'Ингушетия Респ', 'Иркутская обл', 'Кабардино-Балкарская Респ', 'Калининградская обл', 'Калмыкия Респ', 'Калужская обл', 'Камчатский край', 'Карачаево-Черкесская Респ', 'Карелия Респ', 'Кемеровская обл', 'Кировская обл', 'Коми Респ', 'Костромская обл', 'Краснодарский край', 'Красноярский край', 'Курганская обл', 'Курская обл', 'Ленинградская обл', 'Липецкая обл', 'Магаданская обл', 'Марий Эл Респ', 'Мордовия Респ', 'Москва г', 'Московская обл', 'Мурманская обл', 'Ненецкий АО', 'Нижегородская обл', 'Новгородская обл', 'Новосибирская обл', 'Омская обл', 'Оренбургская обл', 'Орловская обл', 'Пензенская обл', 'Пермский край', 'Приморский край', 'Псковская обл', 'Ростовская обл', 'Рязанская обл', 'Самарская обл', 'Санкт-Петербург г', 'Саратовская обл', 'Саха /Якутия/ Респ', 'Сахалинская обл', 'Свердловская обл', 'Северная Осетия - Алания Респ', 'Смоленская обл', 'Ставропольский край', 'Тамбовская обл', 'Татарстан Респ', 'Тверская обл', 'Томская обл', 'Тульская обл', 'Тыва Респ', 'Тюменская обл', 'Удмуртская Респ', 'Ульяновская обл', 'Хабаровский край', 'Хакасия Респ', 'Ханты-Мансийский Автономный округ - Югра АО', 'Челябинская обл', 'Чеченская Респ', 'Чувашская Респ', 'Чукотский АО', 'Ямало-Ненецкий АО', 'Ярославская обл')
