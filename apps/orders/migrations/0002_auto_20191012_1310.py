# Generated by Django 2.0 on 2019-10-12 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='service',
            field=models.CharField(default='', max_length=20, verbose_name='购买服务'),
        ),
    ]
