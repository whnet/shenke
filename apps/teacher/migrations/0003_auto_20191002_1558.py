# Generated by Django 2.0 on 2019-10-02 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0002_auto_20191002_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='mid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_user', to=settings.AUTH_USER_MODEL, verbose_name='老师昵称'),
        ),
        migrations.AddField(
            model_name='services',
            name='tid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_user', to='teacher.Teachers', verbose_name='所属老师'),
        ),
        migrations.AddField(
            model_name='teachers',
            name='mid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_userProfile', to=settings.AUTH_USER_MODEL, verbose_name='老师昵称'),
        ),
        migrations.AddField(
            model_name='teachers',
            name='type',
            field=models.ManyToManyField(blank=True, to='teacher.Categories', verbose_name='老师分类'),
        ),
    ]
