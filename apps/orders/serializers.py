# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
from apps.teacher.models import Services
from django.contrib.auth import get_user_model
from django.db.models import Sum
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化，控制对外提供的字段
    """
    # 微信号做处理 第一个字符 + *** + 最后一个字符
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_nickname(self, obj):
        str = obj.nickname
        nickname = str[0:1]+'***' if len(obj.nickname) == 2 else str[0:1]+'***'+str[-1:]
        return nickname


class TeachersSerializer(serializers.ModelSerializer):
    # 可以实现关联查询，看下面的comments的例子
    mid = UserDetailSerializer()

    class Meta:
        model = Teachers
        fields = '__all__'


class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = '__all__'


class ChatlogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('chatrecord',)

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('id', 'teacher_id',)


class JifenSerializer(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        result = Orders.objects.filter(mid_id=obj.mid,status=5).order_by('id').aggregate(data=Sum('price'))
        return result['data']

    class Meta:
        model = Orders
        fields = ('price','sum')


class WithdrawSerializer(serializers.ModelSerializer):
    # 提现记录
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        result = Withdraw.objects.filter(member_id=obj.member_id).order_by('id').aggregate(data=Sum('price'))
        return result['data']

    class Meta:
        model =  Withdraw
        fields = ('sum','member','openid','price')

class OrdersSerializer(serializers.ModelSerializer):
    # 关联查询对应的ID
    teacher_name = serializers.CharField(source='teacher.realname')
    buy_name = serializers.CharField(source='mid.nickname')
    # 直接格式化输出的时间格式
    created = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # 只更新指定字段
    class Meta:
        model = Orders
        fields = ('comments', 'status', 'ganxie')


class CommentsSerializer(serializers.ModelSerializer):
    # 首页显示10条最新的五星好评，超过20字显示，10位要不一样的老师哦
    # 查找评论，并且可以关联查找属于某个老师
    teacher = TeachersSerializer()
    mid = UserDetailSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'


class TopCommentsSerializer(serializers.ModelSerializer):
    # 首页显示10条最新的五星好评，超过20字显示，10位要不一样的老师哦
    # 查找评论，并且可以关联查找属于某个老师
    teacher = TeachersSerializer()
    mid = UserDetailSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'

