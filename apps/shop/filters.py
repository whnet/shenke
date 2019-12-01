import django_filters

from .models import *


class ShopFilter(django_filters.rest_framework.FilterSet):
    """
    逛逛列表的过滤类
    """
    class Meta:
        model = List
        fields = ('status', )


class CategoryFilter(django_filters.rest_framework.FilterSet):
    """
    逛逛分类的过滤类，是否显示
    """
    class Meta:
        model = Category
        fields = ('status', )