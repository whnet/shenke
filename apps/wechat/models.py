from django.db import models

# Create your models here.


class Wechat(models.Model):
    """
    微信的基础配置
    """
    AppId = models.CharField(max_length=18, blank=True, null=True, verbose_name='AppId')
    AppSecret = models.CharField(max_length=32, blank=True, null=True, verbose_name='AppSecret')
    ApiKey = models.CharField(max_length=32, blank=True, null=True, verbose_name='ApiKey')
    MchID = models.CharField(max_length=18, blank=True, null=True, verbose_name='MchID')
    DOMAIN = models.CharField(max_length=132, blank=True, null=True, verbose_name='DOMAIN')
    status = models.CharField(max_length=1, choices=[('1', '显示'), ('0', '不显示')], verbose_name='状态', default=0)

    class Meta:
        verbose_name = '微信配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '微信配置'
