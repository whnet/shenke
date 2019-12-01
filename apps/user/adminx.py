import xadmin
from .models import *
from xadmin.views.website import LoginView
from xadmin.views import CommAdminView
from xadmin import views
# Register your models here.


class UsersAdmin(object):
    list_display = ('nickname',)


class UserProfileAdmin(object):
    """用来显示用户相关"""
    list_display = ('username','nickname','wechat','created')


class LoginViewAdmin(LoginView):
    """
    定制网站信息

    """
    title = '后台管理系统'


class GlobalSetting(CommAdminView):
    site_title = '后台管理系统'
    site_footer = 'Copyright © 2019 后台管理系统'
    menu_style = 'accordion'


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(LoginView, LoginViewAdmin)
xadmin.site.register(CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
# 先注销UserProfiels, 再重新注册. 先makemigrations xadmin 然后migrate xadmin
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)