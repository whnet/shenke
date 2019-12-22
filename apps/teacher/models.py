from datetime import datetime
from django.db import models
from apps.user.models import UserProfile
from DjangoUeditor.models import UEditorField
from django import forms


class Categories(models.Model):
    """
    老师分类，一个老师可以选择多个服务分类，一个分类属于多个老师：多对多关系，并且前台用户可以创建分类
    """
    title = models.CharField(max_length=10, verbose_name='老师分类')
    sort = models.IntegerField(default=0, verbose_name='排序')
    status = models.CharField(max_length=1, choices=[('1', '显示'), ('0', '不显示')], verbose_name='状态', default=0)
    image = models.ImageField(max_length=200, blank=True, upload_to='category/', verbose_name='图标')

    class Meta:
        verbose_name = '老师分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)


class Teachers(models.Model):
    """
    老师列表
    """
    realname = models.CharField(max_length=10, default='', verbose_name='真实姓名')
    resume = models.TextField(max_length=250, null=True, verbose_name='个人介绍')
    type = models.ManyToManyField(Categories, verbose_name='老师分类', blank=True)
    mid = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                            related_name='teacher_userProfile', null=True, blank=True, verbose_name="老师昵称")
    haopinglv = models.DecimalField(max_digits=8, default=0, decimal_places=2, verbose_name='好评率')
    display = models.CharField(max_length=1, choices=[('1', '上线'), ('0', '下线')], default=0, verbose_name='展示状态')
    online = models.CharField(max_length=1, choices=[('1', '上线'), ('0', '下线')], default=0, verbose_name='上线状态')
    rec = models.CharField(max_length=1, choices=[('1', '推荐'), ('0', '不推荐')], default=0, verbose_name='热推榜')
    honor = models.CharField(max_length=150, null=True, verbose_name='头衔')
    experience = models.CharField(max_length=1000, null=True, verbose_name='经验')
    wechat = models.CharField(max_length=90, null=True, verbose_name='微信号')
    telphone = models.CharField(max_length=11, null=True, verbose_name='手机号')
    area = models.CharField(max_length=180, default='', blank=True, null=False, verbose_name='所在地区')
    star = models.CharField(max_length=10, default='', blank=True, null=False, verbose_name='星座')
    BLOOD_CHOICES = [("A", u"A"),("B", u"B"),("AB", u"AB"),("O", u"O"),("0", u"不知道")]
    bloodtype = models.CharField(max_length=6, blank=True, null=True,
                                 choices=BLOOD_CHOICES, default="", verbose_name="血型")
    GENDER_CHOICES = [("男", u"男"),("女", u"女")]
    sex = models.CharField(max_length=6, blank=True, null=True,
                                 choices=GENDER_CHOICES, default="", verbose_name="性别")
    STATUS_CHOICES = [("1", u"通过"),("2", u"等待审核"),("3", u"拒绝")]
    status = models.CharField(max_length=6, blank=True, null=True,
                                 choices=STATUS_CHOICES, default="0", verbose_name="审核状态")
    msg = models.CharField(max_length=300, null=True, blank=True, verbose_name='审核理由')
    created = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', null=True, blank=True)
    updated = models.DateTimeField(default=datetime.now, null=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '老师列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.realname)


class Services(models.Model):
    """
    一对多关系，一个老师可以有多个服务项目，但这些项目只能是老师自己创建的，所以不是多对多
    """
    title = models.CharField(max_length=50, verbose_name='名称')
    mid = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher_user',
                                null=True, blank=True, verbose_name="老师昵称")
    tid = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name='teacher_user',
                                null=True, blank=True, verbose_name="所属老师")
    proportion = models.DecimalField(default='0.40', decimal_places=2, max_digits=15, verbose_name='分成比例（%）')
    sort = models.IntegerField(default=0, null=True, blank=True, verbose_name='套餐个数')
    belong = models.CharField(max_length=50, null=True, blank=True, verbose_name='所属服务')
    price = models.DecimalField(default=0, decimal_places=2, max_digits=15, verbose_name='服务价格')
    des = models.TextField(default='', blank=True, null=True, verbose_name='服务描述')

    class Meta:
        verbose_name = '服务项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.title)
