# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_blogpost_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
