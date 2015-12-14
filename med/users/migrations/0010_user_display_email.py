# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_email_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='display_email',
            field=models.BooleanField(default=False),
        ),
    ]
