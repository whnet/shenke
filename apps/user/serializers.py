from django.contrib.auth.models import Group
import re
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from apps.user.models import UserProfile
from django.contrib.auth import get_user_model
from apps.teacher.models import Teachers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
     用户详情序列化，控制对外提供的字段
     """
    class Meta:
        model = UserProfile
        fields = ('avatar', 'nickname', 'openid', 'seconds',
                  'sex', 'type', 'wechat', 'year', 'update_status', 'mobile', 'id' )


class UserShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','nickname','avatar', 'upto', 'bindtime', 'sharetime')


class UserShareOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'nickname', 'upto', 'bindtime')


class GroupSerializer(serializers.ModelSerializer):
    """
    用户分组序列化，控制对外提供的字段
    """
    class Meta:
        model = Group
        fields = '__all__'


class TeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachers
        fields = ('mid',)


class ZiliaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'avatar','realname', 'nickname', 'openid', 'seconds',
                  'sex', 'type','year', 'teacher')

    def get_teacher(self, obj):
        teacher = Teachers.objects.filter(mid=obj.id, status= 1)
        if teacher:
            data = {'id': teacher[0].id, 'name':teacher[0].realname}
        else:
            data = {'id': 0, 'msg': '不是老师'}
        return data


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('avatar','realname', 'nickname', 'openid', 'seconds',
                  'sex', 'type', 'update_status', 'year')


class UserOrderSerializer(serializers.ModelSerializer):
    """
    用户详情序列化，控制对外提供的字段
    """
    class Meta:
        model = User
        fields = ('avatar', 'nickname', 'openid', 'seconds',
                  'sex', 'type', 'wechat', 'update_status', 'year', 'mobile', 'id' )


class UserTeacherDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化，控制对外提供的字段test
    """
    class Meta:
        model = User
        fields = ("avatar", 'openid', 'nickname', 'id')
