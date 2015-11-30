# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20151120_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_answer',
            field=models.BooleanField(default=False),
        ),
    ]
