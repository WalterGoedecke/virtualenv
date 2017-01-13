# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0004_auto_20170110_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='Name',
            field=models.CharField(max_length=40, null=True, blank=True, verbose_name="Person's Name"),
        ),
        migrations.AlterField(
            model_name='person',
            name='Person_ID',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
