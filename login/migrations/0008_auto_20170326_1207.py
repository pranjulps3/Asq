# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='display_pic',
            field=models.FileField(upload_to=''),
        ),
    ]
