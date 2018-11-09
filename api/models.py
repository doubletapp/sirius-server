# -*- coding: utf-8 -*-
import uuid as uuid
from django.db import models


class User(models.Model):
    access_token = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.access_token


class Course(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
