# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import med.users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151113_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to=med.users.utils.upload_path, blank=True),
        ),
    ]
