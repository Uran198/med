# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_can_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='can_answer',
        ),
    ]
