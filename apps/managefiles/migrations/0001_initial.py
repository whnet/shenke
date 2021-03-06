# Generated by Django 2.0 on 2019-10-02 15:42

import apps.utils.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(default='', storage=apps.utils.storage.ImageStorage(), upload_to='files/%Y/%m')),
                ('cover', models.ImageField(default='', storage=apps.utils.storage.ImageStorage(), upload_to='files/%Y/%m')),
                ('big', models.ImageField(default='', storage=apps.utils.storage.ImageStorage(), upload_to='files/%Y/%m')),
            ],
            options={
                'verbose_name': '文件管理',
                'verbose_name_plural': '文件管理',
            },
        ),
    ]
