import xadmin
from apps.jifen.models import *
from xadmin.layout import Fieldset


class JifenAdmin(object):
    """
    订单管理
    """
    list_display = ('member','openid','status','plus', 'jifen', 'msg','created',)  # 显示
    list_filter = ['openid']
    # def getopenid(self, obj):
    #     return '%s' % obj.member.nickname  # 可以实现取外键
    # getopenid.short_description = '用户名'

    # xadmin model编辑页隐藏字段
    # form_layout = (
    #     # Fieldset(None,
    #     #          'status','pc_icorn','pc_link','sort'
    #     #          ),
    #     # Fieldset(None,
    #     #          'status',**{"style":"display:None"}
    #     #          ),
    # )

xadmin.site.register(Jifen, JifenAdmin)