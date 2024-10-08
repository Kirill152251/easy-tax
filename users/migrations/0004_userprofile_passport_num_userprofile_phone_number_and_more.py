# Generated by Django 5.0.6 on 2024-08-13 17:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='passport_num',
            field=models.CharField(blank=True, max_length=9, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Incorrect passport number format', regex='[A-Z]{2}\\d{7}')], verbose_name='Номер паспорта'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Incorrect phone format. Correct format: +375*********', regex='\\+375\\d{9}')], verbose_name='Мобильный номер'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_address',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес регистрации'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='residential_address',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Адрес проживания'),
        ),
    ]
