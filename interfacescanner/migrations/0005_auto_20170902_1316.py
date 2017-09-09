# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-02 05:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interfacescanner', '0004_auto_20170902_1248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interface',
            options={'ordering': ['-created_time']},
        ),
        migrations.RemoveField(
            model_name='interface',
            name='discription',
        ),
        migrations.AddField(
            model_name='interface',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='\u63a5\u53e3\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='interface',
            name='proxy',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='\u4ee3\u7406\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='interface',
            name='theurl',
            field=models.URLField(max_length=500, unique=True, verbose_name='\u63a5\u53e3url'),
        ),
    ]
