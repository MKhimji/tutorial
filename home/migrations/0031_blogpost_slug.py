# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-23 01:07
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields



class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_remove_blogpost_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='title', unique=True),
        ),
    ]
