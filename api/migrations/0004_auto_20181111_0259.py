# Generated by Django 2.1.3 on 2018-11-11 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181111_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkuser',
            name='educational_feed',
            field=models.ManyToManyField(related_name='educational_feed_courses', to='api.Course'),
        ),
        migrations.AddField(
            model_name='vkuser',
            name='educational_trajectory',
            field=models.ManyToManyField(related_name='educational_trajectory_courses', to='api.CourseTemplate'),
        ),
    ]
