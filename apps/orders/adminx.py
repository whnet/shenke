import xadmin
from apps.orders.models import *


class OrderAdmin(object):
    """
    订单管理
    """
    list_display = ('title', 'teacher', 'price', 'status')  # 显示
    search_fields = ('title', 'chatrecord',)  # 搜索
    list_filter = ('status',)  # 过滤
    exclude = ['chat','type'] # 设置详情页面不显示某个字段
    style_fields = {"chat": "ueditor"}
    readonly_fields = ['type', 'status']


class WithdrawAdmin(object):
    list_display = ('member', 'price', 'status', 'created', 'payment_time')  # 显示
    search_fields = ('member', 'price', 'partner_trade_no', 'payment_no', 'payment_time', 'status', 'created')  # 搜索


class ChatsAdmin(object):
    list_display = ('title', 'teacher', 'price', 'status')  # 显示


xadmin.site.register(Orders, OrderAdmin)
xadmin.site.register(Withdraw, WithdrawAdmin)