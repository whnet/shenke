# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
from apps.orders.models import Orders


class WechatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wechat
        fields = '__all__'


class WechatNotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = '__all__'