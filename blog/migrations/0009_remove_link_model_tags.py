# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 05:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180329_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='model_tags',
        ),
    ]
