# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0005_auto_20150909_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='doc',
            field=models.CharField(null=True, max_length=80, blank=True),
        ),
    ]
