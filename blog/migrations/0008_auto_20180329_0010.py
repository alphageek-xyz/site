# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 05:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_link_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='tags',
            new_name='model_tags',
        ),
    ]
