# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-19 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20170919_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_body',
            field=models.TextField(default='exit'),
            preserve_default=False,
        ),
    ]
