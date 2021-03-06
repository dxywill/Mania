# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 03:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0002_auto_20170621_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('gender', models.IntegerField()),
                ('diagnosis', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='survey',
            name='age',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='diagnosis',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='sex',
        ),
        migrations.AddField(
            model_name='survey',
            name='state',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
