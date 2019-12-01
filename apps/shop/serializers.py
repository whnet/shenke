# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
from apps.orders.models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化，控制对外提供的字段
    """
    # 微信号做处理 第一个字符 + *** + 最后一个字符
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('avatar','name', 'id')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        buy = Orders.objects.filter(teacher=obj.id,status=5).count()
        ganxie = Orders.objects.filter(teacher=obj.id,status=5,ganxie=1).count()
        data = {
            'buy': buy,
            'ganxie': ganxie,
        }
        return data

    class Meta:
        model = List
        fields = '__all__'
