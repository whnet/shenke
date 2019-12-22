# Generated by Django 2.0 on 2019-12-22 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_auto_20191220_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='proportion',
            field=models.DecimalField(decimal_places=2, default='0.40', max_digits=15, verbose_name='分成比例（%）'),
        ),
    ]