# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-04 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification_channels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='action_obj_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='generator_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]