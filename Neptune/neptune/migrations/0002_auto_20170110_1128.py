# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='Name',
            field=models.CharField(max_length=40, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='Person_ID',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
