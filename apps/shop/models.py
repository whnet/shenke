from datetime import datetime
from django.db import models
from apps.user.models import UserProfile
from apps.teacher.models import Teachers
from DjangoUeditor.models import UEditorField
 

class Category(models.Model):
    """
    逛逛产品分类：闪测、产品、课程
    """
    title = models.CharField(max_length=40, verbose_name='名称')
    note = models.CharField(max_length=30, verbose_name='标志符', null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.CharField(max_length=1, choices=[('1', '显示'), ('0', '不显示')], verbose_name='状态', default=0)

    class Meta:
        verbose_name = '逛逛分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class List(models.Model):
    """
    逛逛列表页
    """
    title = models.CharField(max_length=40, blank=True, null=True, verbose_name='名称')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='价格')
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='shop_Teachers',
                                null=True, blank=True, verbose_name="所属老师")
    mid = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shop_userProfile',
                            null=True, blank=True, verbose_name="老师昵称")
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.CharField(max_length=1, choices=[('1', '显示'), ('0', '不显示')], verbose_name='状态', default=0)
    cover = models.CharField(max_length=140, blank=True, null=True,  verbose_name='封面图')
    big =  models.CharField(max_length=140, blank=True, null=True,  verbose_name='大图')
    des = models.TextField(max_length=300, blank=True, null=True, verbose_name='简介')
    detail = models.TextField(max_length=300, blank=True, null=True, verbose_name='详情')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', null=True, blank=True)

    class Meta:
        verbose_name = '应用列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
