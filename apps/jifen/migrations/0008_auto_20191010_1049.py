# Generated by Django 2.0 on 2019-10-10 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jifen', '0007_auto_20191009_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jifen',
            name='plus',
            field=models.CharField(blank=True, choices=[('1', '增加'), ('2', '减少')], default='2', max_length=1, null=True, verbose_name='积分增减'),
        ),
    ]
