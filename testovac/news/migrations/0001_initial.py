# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'publication date')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(help_text=b'Content will be interpreted via <a href="http://en.wikipedia.org/wiki/Markdown">Markdown</a>.')),
                ('author', models.ForeignKey(related_name='news_entries', to=settings.AUTH_USER_MODEL)),
                ('competitions', models.ManyToManyField(to='tasks.Competition')),
            ],
            options={
                'ordering': ('-pub_date',),
                'get_latest_by': 'pub_date',
                'verbose_name': 'announcement',
                'verbose_name_plural': 'announcements',
            },
        ),
    ]
