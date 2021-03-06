# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-07 14:48
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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(blank=True, max_length=40)),
                ('key_expires', models.DateTimeField(blank=True, null=True)),
                ('sex', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unsure')], max_length=1)),
                ('age', models.PositiveIntegerField()),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('url', models.CharField(blank=True, max_length=50, null=True)),
                ('job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('id_no', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=255, null=True)),
                ('profile', models.TextField(blank=True, max_length=256, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('S', 'Single'), ('M', 'Married')], max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]
