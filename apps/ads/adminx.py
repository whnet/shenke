import xadmin
from .models import *
# Register your models here.


class AdsAdmin(object):
    """
     广告列表
    """
    list_display = ('title', 'status', 'online', 'offline', 'sort')  # 显示
    search_fields = ('title', 'status', 'online', 'offline', 'sort')  # 搜索
    list_filter = ('status',)  # 过滤
    style_fields = {'type': 'checkbox-inline', }


class TypeAdmin(object):
    """
    广告类型
    """
    list_display = ('title', 'status', 'sort')  # 显示
    search_fields = ('title', 'status', 'sort')  # 搜索
    list_filter = ('status',)  # 过滤


xadmin.site.register(Ads, AdsAdmin)
xadmin.site.register(Type, TypeAdmin)