# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-28 22:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180328_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='tags',
        ),
    ]
