# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_question_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='update_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
