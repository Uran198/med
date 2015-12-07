# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20151207_1516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('-pub_date',)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-pub_date',)},
        ),
    ]
