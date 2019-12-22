from django.db import models
from apps.teacher.models import Teachers, Services
from apps.user.models import UserProfile


# 订单列表关联老师列表
class Orders(models.Model):
    STATUS_CHOICE = [('-1', '拒单'), ('0', '未付款'), ('1', '待接单'),('2', '已退款'), ('3', '进行中'),('4', '待评价'), ('5', '已完成')]
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='名称')
    upto = models.CharField(max_length=100, null=True, blank=True, verbose_name='上级')
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='teachers',
                                null=True, blank=True, verbose_name="所属老师", default=0)
    tomember = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='userProfile',
                                null=True, blank=True, verbose_name="所属老师昵称")
    mid = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_userProfile',
                                null=True, blank=True, verbose_name="购买用户")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='金额')
    type = models.CharField(max_length=20, verbose_name='订单类型', default='')
    out_trade_no = models.CharField(max_length=100, verbose_name='订单号', default=0)
    status = models.CharField(max_length=5,
                              choices=STATUS_CHOICE,
                              verbose_name='状态', default=0)
    proportion = models.DecimalField(default='0.40', decimal_places=2, max_digits=15, verbose_name='分成比例（%）')
    detail = models.TextField(max_length=1000, verbose_name='订单备注', blank=True, default='')
    ganxie = models.CharField(max_length=1,choices=[('0', '未感谢'), ('1', '已感谢')],verbose_name='是否感谢', default=0)
    belong = models.CharField(max_length=100,choices=[('0', '非套餐'), ('1', '套餐')],verbose_name='是否感谢', default=0)
    taocan = models.IntegerField(default=0, verbose_name='是否是套餐')
    kaiqi = models.IntegerField(default=0, verbose_name='是否开启订单')
    pid = models.IntegerField(default=0, verbose_name='所属问题')
    comments = models.TextField(max_length=500, verbose_name='评价', blank=True, default='')
    chatrecord = models.TextField(verbose_name='聊天记录', blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', null=True, blank=True)

    class Meta:
        verbose_name='订单列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Withdraw(models.Model):
    STATUS_CHOICE = [('0', '未打款'), ('1', '已结款')]
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='withdraw_userProfile',
                                null=True, blank=True, verbose_name="提现用户")
    openid = models.CharField(max_length=50, verbose_name='用户识别码', blank=True, default='')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='金额')
    partner_trade_no = models.CharField(max_length=32, verbose_name='商户订单号', blank=True, default='')
    payment_no = models.CharField(max_length=64, verbose_name='微信付款单号', blank=True, default='')
    payment_time = models.CharField(max_length=32, verbose_name='付款成功时间', blank=True, default='')
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICE,
                              verbose_name='状态', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='申请时间', null=True, blank=True)

    class Meta:
        verbose_name='提现列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.openid
