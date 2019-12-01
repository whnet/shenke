import xadmin
from .models import *
# Register your models here.


class WechatAdmin(object):
    """
     广告列表
    """
    list_display = ('AppId', 'AppSecret', 'ApiKey', 'MchID')  # 显示
    search_fields = ('AppId', 'AppSecret', 'ApiKey', 'MchID')  # 搜索

# xadmin.site.register(Wechat, WechatAdmin)