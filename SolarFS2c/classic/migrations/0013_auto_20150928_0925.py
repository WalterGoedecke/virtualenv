# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0012_holiday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculation',
            name='begin',
            field=models.DateField(max_length=30, null=True),
        ),
    ]
