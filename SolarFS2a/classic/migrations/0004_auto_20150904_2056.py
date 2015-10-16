# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0003_calculation'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='B',
            field=models.CharField(max_length=80, blank=True, default='B', null=True),
        ),
        migrations.AlterField(
            model_name='calculation',
            name='A',
            field=models.CharField(max_length=80, blank=True, default='A', null=True),
        ),
    ]
