# Generated by Django 2.0 on 2019-12-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20191002_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachers',
            name='rec',
            field=models.CharField(choices=[('1', '推荐'), ('0', '不推荐')], default=0, max_length=1, verbose_name='热推榜'),
        ),
    ]
