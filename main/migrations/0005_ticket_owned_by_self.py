# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_ticket_used_by_self'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='owned_by_self',
            field=models.BooleanField(default=True),
        ),
    ]
