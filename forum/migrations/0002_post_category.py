# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-28 17:49
from __future__ import unicode_literals

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
    ]
