# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classic', '0014_auto_20150928_1120'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Holiday',
        ),
    ]
