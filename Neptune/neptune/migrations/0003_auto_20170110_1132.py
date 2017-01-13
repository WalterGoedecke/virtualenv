# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neptune', '0002_auto_20170110_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='Address',
            field=models.TextField(unique=True, verbose_name='Place_ID', max_length=120),
        ),
    ]
