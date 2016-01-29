# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='competition name')),
                ('public', models.BooleanField(default=True, verbose_name='competition is public')),
                ('user_groups', models.ManyToManyField(to='auth.Group', verbose_name='user groups')),
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
                ('start_time', models.DateTimeField(default=datetime.datetime(2016, 1, 29, 15, 0))),
                ('end_time', models.DateTimeField(default=datetime.datetime(2016, 1, 29, 15, 0))),
                ('visible', models.BooleanField(default=False)),
                ('competition', models.ForeignKey(to='tasks.Competition')),
            ],
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
        ),
    ]
