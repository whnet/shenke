import xadmin
from .models import *
# Register your models here.


class ListAdmin(object):
    """
     广告列表
    """
    list_display = ('title', 'teacher', 'price', 'status', 'proportion')  # 显示
    search_fields = ('title', 'status', 'teacher__realname' )  # 搜索
    # list_filter = ('status',)  # 过滤
    style_fields = {"detail": "ueditor"}


class CategoryAdmin(object):
    """
    广告类型
    """
    list_display = ('title', 'status', 'sort')  # 显示
    search_fields = ('title', 'status', 'sort')  # 搜索
    list_filter = ('status',)  # 过滤


xadmin.site.register(List, ListAdmin)
# xadmin.site.register(Category, CategoryAdmin)