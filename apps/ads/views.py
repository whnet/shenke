from rest_framework import mixins
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend


class AdsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    广告列表
    """
    queryset = Ads.objects.all().order_by("-id")
    serializer_class = AdsSerializer
    # 设置三大常用过滤器之DjangoFilterBackend, SearchFilter filters.OrderingFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    # 设置我们的search字段
    search_fields = ('title',)
    # 设置我们需要进行过滤的字段
    filter_fields = ('title', 'type', )


class TypeListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    广告类型
    """
    queryset = Type.objects.all().order_by("-id")
    serializer_class = TypeSerializer
