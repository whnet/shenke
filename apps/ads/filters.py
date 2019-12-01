import django_filters

from .models import *


class AdsFilter(django_filters.rest_framework.FilterSet):
    """
    老师的过滤类
    """
    title = django_filters.CharFilter(name='title', help_text="老师名字", lookup_expr='icontains',)

    class Meta:
        model = Ads
        fields = ('title',)