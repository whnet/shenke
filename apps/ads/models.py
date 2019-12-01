from datetime import datetime
from django.db import models


class Type(models.Model):
    """
    广告类型
    """
    title = models.CharField(max_length=30, verbose_name='名称')
    type = models.CharField(max_length=30, verbose_name='广告类型', null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.CharField(max_length=1, choices=[('1', '显示'), ('0', '不显示')], verbose_name='状态', default=0)

    class Meta:
        verbose_name = '广告类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Ads(models.Model):
    """
    广告应用：BANNER图、公告等都属于广告
    """
    title = models.CharField(max_length=100, verbose_name='名称')
    type = models.ManyToManyField(Type, verbose_name='广告类别', blank=True)
    status = models.CharField(max_length=1, choices=[('1', '显示'), ('0', '不显示')], verbose_name='状态', default=0)
    online = models.DateTimeField(default=datetime.now, verbose_name='上线时间')
    offline = models.DateTimeField(default=datetime.now, verbose_name='下线时间')
    image = models.ImageField(max_length=200, blank=True, upload_to='ads/', verbose_name='图片')
    url = models.URLField(max_length=500, null=True, verbose_name='链接', blank=True)
    sort = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


