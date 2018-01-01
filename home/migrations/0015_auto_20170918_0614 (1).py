# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-18 05:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20170918_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_name', models.CharField(max_length=64)),
                ('comment_body', models.TextField()),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_blogpost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.BlogPost'),
        ),
    ]
