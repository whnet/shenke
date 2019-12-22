# Generated by Django 2.0 on 2019-12-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20191220_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='proportion',
            field=models.DecimalField(decimal_places=2, default='40.00', max_digits=15, verbose_name='分成比例（%）'),
        ),
    ]
