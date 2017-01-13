# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0003_auto_20170110_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='Address',
            field=models.CharField(verbose_name='Place_ID', unique=True, max_length=120),
        ),
    ]
