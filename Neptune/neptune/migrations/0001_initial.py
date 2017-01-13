# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('Name', models.TextField(blank=True, max_length=40, null=True)),
                ('Person_ID', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('Address', models.TextField(verbose_name='Place_ID', max_length=120, blank=True, null=True)),
                ('Latitude', models.CharField(verbose_name='GPS Latitude - leave blank', max_length=16, blank=True, null=True)),
                ('Longitude', models.CharField(verbose_name='GPS Longitude - leave blank', max_length=16, blank=True, null=True)),
                ('Address_Name', models.ManyToManyField(verbose_name="Name, e.g., Fred's Place", blank=True, to='neptune.Person')),
            ],
        ),
    ]
