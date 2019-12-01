# Generated by Django 2.0 on 2019-11-12 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_withdraw'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdraw',
            name='name',
        ),
        migrations.AddField(
            model_name='withdraw',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='withdraw_userProfile', to=settings.AUTH_USER_MODEL, verbose_name='提现用户'),
        ),
    ]
