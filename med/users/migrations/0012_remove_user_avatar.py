# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20151214_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]
