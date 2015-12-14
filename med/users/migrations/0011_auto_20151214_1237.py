# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_display_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_email',
            field=models.BooleanField(default=False, verbose_name='Display email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_notifications',
            field=models.BooleanField(default=True, verbose_name='Email Notifications'),
        ),
    ]
