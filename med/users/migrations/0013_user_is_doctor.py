# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(default=False, verbose_name='Is a Doctor'),
        ),
    ]
