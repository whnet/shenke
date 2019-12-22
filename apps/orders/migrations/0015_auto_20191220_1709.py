# Generated by Django 2.0 on 2019-12-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_remove_withdraw_proportion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('-1', '拒单'), ('0', '未付款'), ('1', '待接单'), ('2', '已退款'), ('3', '进行中'), ('4', '待评价'), ('5', '已完成')], default=0, max_length=5, verbose_name='状态'),
        ),
    ]