# Generated by Django 2.0 on 2019-12-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20191220_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraw',
            name='proportion',
            field=models.DecimalField(decimal_places=2, default='40.00', max_digits=15, verbose_name='分成比例（%）'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='openid',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='用户识别码'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='partner_trade_no',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='商户订单号'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='payment_no',
            field=models.CharField(blank=True, default='', max_length=64, verbose_name='微信付款单号'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='payment_time',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='付款成功时间'),
        ),
    ]