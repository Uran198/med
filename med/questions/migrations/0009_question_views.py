# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20151207_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
