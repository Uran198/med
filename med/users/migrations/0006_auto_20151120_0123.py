# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import med.users.utils
import med.users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20151119_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, validators=[med.users.validators.validate_file_size], upload_to=med.users.utils.upload_path),
        ),
    ]
