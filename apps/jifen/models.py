from django.db import models
from apps.user.models import UserProfile

# Create your models here.


class Jifen(models.Model):
    STATUS_CHOICE = [('0', '待审核'), ('1', '已通过'), ('2', '拒绝')]
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_member',
                                null=True, blank=True, verbose_name="所属会员")
    openid = models.CharField(max_length=100, null=True, blank=True, verbose_name='识别码')
    plus = models.CharField(max_length=1,
                              choices=[('1', '增加'),('2', '减少'),],
                              verbose_name='积分增减', null=True, blank=True, default='2')
    jifen = models.DecimalField(default=0, decimal_places=2, max_digits=15, null=True, blank=True, verbose_name='积分')
    msg = models.CharField(max_length=100, null=True, blank=True, verbose_name='操作原因')
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICE,
                              verbose_name='状态', null=True, blank=True, default='0')
    created = models.DateTimeField(auto_now_add=True, verbose_name='操作时间', null=True, blank=True)

    class Meta:
        db_table = "jifen"
        verbose_name='积分核销'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.openid
