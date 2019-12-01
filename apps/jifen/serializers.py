from rest_framework import serializers
from .models import Jifen
from django.contrib.auth import get_user_model
from django.db.models import Sum
User = get_user_model()


class JifenSerializer(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        result = Jifen.objects.filter(member_id=obj.member_id,status=1).order_by('id').aggregate(data=Sum('jifen'))
        return result['data']

    class Meta:
        model = Jifen
        fields = ('jifen','sum','msg','plus')


class JifenAddSerializer(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        result = Jifen.objects.filter(member_id=obj.member_id,status=1).order_by('id').aggregate(data=Sum('jifen'))
        return result['data']

    class Meta:
        model = Jifen
        fields = ('member','openid','sum','jifen')