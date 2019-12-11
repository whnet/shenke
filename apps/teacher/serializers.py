# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
from apps.user.models import UserProfile
from apps.orders.models import Orders
from django.db.models import Q


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
        # exclude 为不展示的字段名，和 fields 不能同时设置
        # exclude = ['id', 'author']


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        # result 接口需要返回的字段，可以指定 "__all__" 展示全部参数
        fields = '__all__'


class UpdateTeacherSerializer(serializers.ModelSerializer):
    type = CategoriesSerializer(many=True, read_only=True)
    class Meta:
        model = Teachers
        fields = '__all__'


class TeacherDetailSerializer(serializers.ModelSerializer):
    # 关联查询对应的ID
    type = CategoriesSerializer(many=True, read_only=True)
    avatar = serializers.CharField(source='mid.avatar')
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        jieda = Orders.objects.filter(teacher=obj.id,status=5).count()
        ganxie = Orders.objects.filter(teacher=obj.id,ganxie=1,status=5).count()
        # 找到服务中价格最小的
        services_count = Services.objects.filter(tid_id=obj.id).count()
        if services_count:
            service = Services.objects.filter(tid_id=obj.id).order_by('price').values()
            price = service[0]['price']
        else:
            price = '0.00'
        data = {
            'jieda': jieda,
            'ganxie': ganxie,
            'price':price,
            'services_count': services_count
        }
        return data

    class Meta:
        model = Teachers
        exclude = ['area', 'wechat','bloodtype','msg','online','telphone','updated','display','created','star','status']


class TInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachers
        exclude = ['area', 'wechat', 'bloodtype', 'msg', 'online', 'telphone', 'updated', 'display',
                   'created', 'rec', 'star', 'status']


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachers
        exclude = ['area', 'wechat', 'bloodtype', 'msg', 'online', 'telphone', 'updated', 'display',
                   'created', 'star', 'status']
