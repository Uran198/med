# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_question_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Publish date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='questions.Question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_date',
            field=models.DateTimeField(verbose_name='Update date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent', related_name='comment_set', to='questions.Answer'),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Publish date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='update_date',
            field=models.DateTimeField(verbose_name='Update date', auto_now=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Is Closed'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Publish date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from='title', verbose_name='Slug', editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='questions.Tag', verbose_name='Tags', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='question',
            name='update_date',
            field=models.DateTimeField(verbose_name='Update date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Views'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='parent',
            field=models.ForeignKey(verbose_name='Parent', related_name='comment_set', to='questions.Question'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Publish date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='update_date',
            field=models.DateTimeField(verbose_name='Update date', auto_now=True),
        ),
    ]
