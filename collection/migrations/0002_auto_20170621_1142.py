# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-21 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('sex', models.IntegerField()),
                ('feelings', models.IntegerField()),
                ('diagnosis', models.IntegerField()),
                ('medications', models.CharField(max_length=200)),
                ('substances', models.IntegerField()),
                ('flash', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='eyeimage',
            name='dateTime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eyeimage',
            name='image_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='survey',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.EyeImage'),
        ),
    ]
