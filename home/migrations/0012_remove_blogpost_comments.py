# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 01:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_blogpost_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='comments',
        ),
    ]
