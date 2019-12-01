# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *
__author__ = 'yl'


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'


class AdsSerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = Ads
        fields = '__all__'
