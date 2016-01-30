# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('public', models.BooleanField(default=True)),
                ('users_group', models.ForeignKey(blank=True, to='auth.Group', null=True)),
            ],
            options={
                'verbose_name': 'competition',
                'verbose_name_plural': 'competitions',
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('number', models.IntegerField()),
                ('start_time', models.DateTimeField(default=datetime.datetime(2016, 1, 30, 17, 0, tzinfo=utc))),
                ('end_time', models.DateTimeField(default=datetime.datetime(2016, 1, 30, 17, 0, tzinfo=utc))),
                ('visible', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(to='tasks.Competition')),
            ],
            options={
                'verbose_name': 'contest',
                'verbose_name_plural': 'contests',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('number', models.IntegerField()),
                ('max_points', models.IntegerField()),
                ('contest', models.ForeignKey(to='tasks.Contest')),
            ],
            options={
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
        ),
    ]
