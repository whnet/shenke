import xadmin
from .models import *
# Register your models here.


class TeachersAdmin(object):
    """
     老师列表
    """
    # readonly_fields = ('services',) # 通过这个只显示输入自己的服务项目，没办法。
    # fileds, exclude 分别控制是否在后台显示该字段
    # exclude = ['haoping',]
    list_display = ('realname', 'honor', 'experience', 'status')  # 显示
    # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
    # list_display_links = ('id', 'underwriter')
    search_fields = ('realname', 'we_chat', 'experience', 'resume')  # 搜索
    list_filter = ('display',)  # 过滤
    style_fields = {'type': 'checkbox-inline', "detail": "ueditor"}
    # style_fields = {'type': 'checkbox-inline', 'services': 'checkbox-inline', "detail": "ueditor"}


class CategoriesAdmin(object):
    """
    服务分类
    """
    list_display = ('title', 'sort', 'status')
    search_fields = ('title',)
    list_filter = ('status',)


class ServicesAdmin(object):
    """
    服务项目
    """
    list_display = ('title', 'price', 'tid', 'mid', 'proportion')
    search_fields = ('title', 'tid__realname', 'mid__nickname')
    # 设置详情页面不显示某个字段
    exclude=['sort', 'belong']

"""
同一个APP下，界面上的顺序和注册顺序一致
"""
xadmin.site.register(Teachers, TeachersAdmin)
xadmin.site.register(Categories, CategoriesAdmin)
xadmin.site.register(Services, ServicesAdmin)
