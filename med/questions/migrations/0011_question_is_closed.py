# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20151221_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
