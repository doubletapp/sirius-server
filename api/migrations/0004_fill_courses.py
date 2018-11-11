import csv
import os
from collections import namedtuple

from django.db import migrations

from api.models import CourseTemplate


def read_rows():
    with open(os.path.join(os.path.dirname(__file__), 'data/CoursesSheet1.csv'), encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
        Row = namedtuple('Row', header)
        for row in csv_reader:
            yield Row(*row)


def fill(apps, schema_editor):
    for row in read_rows():
        CourseTemplate(
            title=row.title,
            course_type=row.course_type,
            regularity=row.regularity,
            class_start=int(row.class_start),
            class_end=int(row.class_end),
            intramuraled=row.intramuraled,
            command=row.command,
            url=row.url,
        ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_auto_20181111_0229'),
    ]

    operations = [
        migrations.RunPython(fill),
    ]
