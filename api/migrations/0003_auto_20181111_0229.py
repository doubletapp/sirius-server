# Generated by Django 2.1.3 on 2018-11-11 02:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181110_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('course_type', models.CharField(choices=[('club', 'club'), ('competition', 'competition'), ('activity', 'activity')], max_length=200)),
                ('regularity', models.CharField(blank=True, max_length=400, null=True)),
                ('class_start', models.IntegerField(default=5)),
                ('class_end', models.IntegerField(default=11)),
                ('intramuraled', models.CharField(choices=[('intramural', 'intramural'), ('extramural', 'extramural'), ('online', 'online')], max_length=200)),
                ('command', models.CharField(choices=[('command', 'command'), ('personal', 'personal')], max_length=200)),
                ('url', models.URLField()),
                ('specialization', models.CharField(choices=[('math', 'math'), ('history', 'history'), ('programming', 'programming')], max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='title',
        ),
        migrations.AddField(
            model_name='course',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='course',
            name='course_template',
            field=models.ForeignKey(null=True, on_delete=True, to='api.CourseTemplate'),
        ),
    ]