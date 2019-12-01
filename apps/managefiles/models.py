from django.db import models
from apps.utils.storage import ImageStorage


class Upload(models.Model):
    file = models.ImageField(upload_to='files/%Y/%m', default='', storage=ImageStorage())
    cover = models.ImageField(upload_to='files/%Y/%m', default='', storage=ImageStorage())
    big = models.ImageField(upload_to='files/%Y/%m', default='', storage=ImageStorage())

    class Meta:
        verbose_name='文件管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file