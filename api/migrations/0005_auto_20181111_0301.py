# Generated by Django 2.1.3 on 2018-11-11 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20181111_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuser',
            name='educational_feed',
            field=models.ManyToManyField(blank=True, null=True, related_name='educational_feed_courses', to='api.Course'),
        ),
        migrations.AlterField(
            model_name='vkuser',
            name='educational_trajectory',
            field=models.ManyToManyField(blank=True, null=True, related_name='educational_trajectory_courses', to='api.CourseTemplate'),
        ),
    ]
