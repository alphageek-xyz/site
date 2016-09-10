# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-11 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='html',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='HTML Markup'),
            preserve_default=False,
        ),
    ]
