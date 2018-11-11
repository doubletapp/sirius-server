import csv
import os
from collections import namedtuple

from django.db import migrations

from api.models import CourseTemplate


def read_rows():
    with open(os.path.join(os.path.dirname(__file__), 'data/sirius_recomendations.txt'), encoding='utf-8') as csvfile:
        # csv_reader = csv.reader(csvfile)
        for row in csvfile:
            yield row.rsplit('\n')[0]


def fill(apps, schema_editor):
    for title in read_rows():
        print(len(title))
        CourseTemplate(
            title=title[:200],
            course_type='unknown',
            regularity='',
            class_start=5,
            class_end=11,
            intramuraled='unknown',
            command='unknown',
            url='',
            source='sirius',
        ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_fill_courses'),
    ]

    operations = [
        migrations.RunPython(fill),
    ]
