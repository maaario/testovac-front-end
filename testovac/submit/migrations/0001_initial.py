# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('filename', models.CharField(max_length=128, blank=True)),
                ('type', models.IntegerField(choices=[(0, b'source'), (1, b'description'), (2, b'testable_zip'), (3, b'external')])),
                ('points', models.DecimalField(max_digits=5, decimal_places=2)),
                ('manually_approved', models.BooleanField()),
                ('testing_finished', models.BooleanField()),
                ('tester_response', models.CharField(max_length=10, blank=True)),
                ('reviewed', models.BooleanField()),
                ('reviewer_comment', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'submit',
                'verbose_name_plural': 'submits',
            },
        ),
        migrations.CreateModel(
            name='SubmitReceiver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_source', models.BooleanField()),
                ('has_description', models.BooleanField()),
                ('has_testable_zip', models.BooleanField()),
                ('has_external', models.BooleanField()),
                ('source_points', models.IntegerField()),
                ('description_points', models.IntegerField()),
                ('testable_zip_points', models.IntegerField()),
                ('external_points', models.IntegerField()),
                ('external_submit_link', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'submit receiver',
                'verbose_name_plural': 'submit receivers',
            },
        ),
        migrations.AddField(
            model_name='submit',
            name='receiver',
            field=models.ForeignKey(to='submit.SubmitReceiver'),
        ),
        migrations.AddField(
            model_name='submit',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
