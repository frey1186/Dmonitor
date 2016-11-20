# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-30 07:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('address', models.GenericIPAddressField(verbose_name='IP地址')),
                ('status', models.CharField(choices=[('Online', '在线'), ('Offline', '掉线'), ('Unreachable', '不可达'), ('Maintenance', '维护')], max_length=64, verbose_name='状态')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
