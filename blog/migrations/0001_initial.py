# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('content', models.TextField(blank=True)),
                ('order', models.IntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
    ]
