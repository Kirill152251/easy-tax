# Generated by Django 5.0.6 on 2024-06-14 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='secret_word',
            field=models.CharField(blank=True),
        ),
    ]