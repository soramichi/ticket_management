# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Live',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('live_name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=512, null=True)),
                ('number', models.IntegerField(default=0, verbose_name='number of tickets you have')),
                ('live', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Live')),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_name', models.CharField(max_length=512)),
                ('artist_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='live',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Tour'),
        ),
    ]
