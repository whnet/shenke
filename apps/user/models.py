from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户，在原有数据表上新增的字段
    """
    id = models.AutoField(primary_key = True)
    GENDER_CHOICES = [("男", u"男"),("女", u"女")]
    AVATAR_STATUS_CHOICES = [("1", u"更改"),("0", u"未变"),]
    nickname = models.CharField(max_length=130, blank=True, default='', null=True, verbose_name='昵称')
    avatar = models.CharField(max_length=230, blank=True, null=True, verbose_name='用户头像')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话", help_text="电话号码")
    sex = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES, default="", verbose_name="性别")
    type = models.CharField(max_length=100, null=True, blank=True, verbose_name="日期类型")
    year = models.CharField(max_length=100, null=True, blank=True, verbose_name="年月日")
    realname = models.CharField(max_length=100, null=True, blank=True, verbose_name="真实姓名")
    seconds = models.CharField(max_length=100, null=True, blank=True, verbose_name="时辰")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    openid = models.CharField(max_length=28, verbose_name='OPENID', blank=True, null=True)
    wechat = models.CharField(max_length=30, null=True, verbose_name='微信号', blank=True)
    upto = models.CharField(max_length=30, null=True, verbose_name='上级', default='0', blank=True)
    sharetime = models.CharField(max_length=30, null=True, verbose_name='分享时间', default='0', blank=True)
    bindtime = models.CharField(max_length=30, null=True, verbose_name='绑定时间', default='0', blank=True)
    # 是否更新过头像
    update_status = models.CharField(max_length=6, blank=True, null=True,
                                 choices=AVATAR_STATUS_CHOICES, default="0", verbose_name="更改状态")
    created = models.DateTimeField(auto_now_add=True, verbose_name='注册时间', null=True, blank=True)

    class Meta:
        verbose_name = '用户列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.nickname)

