# Generated by Django 2.0 on 2019-12-20 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20191220_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdraw',
            name='proportion',
        ),
    ]
