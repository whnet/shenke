# -*- coding: utf-8 -*-

"""
微信公众号和商户平台信息配置文件
"""


# ----------------------------------------------微信公众号---------------------------------------------- #
# 公众号appid
APPID = 'wx46b3ddbed629ab60'
# 公众号AppSecret
APPSECRET = 'b48686496d6a5eedc51cbcd967ab35df'


# ----------------------------------------------微信商户平台---------------------------------------------- #
# 商户id
MCH_ID = '1402693502'
API_KEY = 'X7nQ0NbRLsinSe4JRzQdLRRI0RsiGX0s'
Notify_url = 'http://xrbz6c.natappfree.cc/wechatnotify/'

# ----------------------------------------------七牛平台---------------------------------------------- #
QINIU_Ak = 'QEjVuwzVxzcj2yBU08pwbhYRnnDSJp5rpp6ZA52r'
QINIU_Sk = 'wj9nbDqNq0filDnXKdaBPwnwZVxJWyjMJWCNuEV6'


# ----------------------------------------------回调页面---------------------------------------------- #
# 用户授权获取code后的回调页面，如果需要实现验证登录就必须填写
REDIRECT_URI = 'http://bangce.emifo.top/#/scrope'
PC_LOGIN_REDIRECT_URI = 'http://bangce.emifo.top/#/scrope'

defaults = {
    # 微信内置浏览器获取code微信接口
    'wechat_browser_code': 'https://open.weixin.qq.com/connect/oauth2/authorize',
    # 微信内置浏览器获取access_token微信接口
    'wechat_browser_access_token': 'https://api.weixin.qq.com/sns/oauth2/access_token',
    # 微信内置浏览器获取用户信息微信接口
    'wechat_browser_user_info': 'https://api.weixin.qq.com/sns/userinfo',
    # pc获取登录二维码接口
    'pc_QR_code': 'https://open.weixin.qq.com/connect/qrconnect',
    # 获取微信公众号access_token接口
    'mp_access_token': 'https://api.weixin.qq.com/cgi-bin/token',
    # 设置公众号行业接口
    'change_industry': 'https://api.weixin.qq.com/cgi-bin/template/api_set_industry',
    # 获取公众号行业接口
    'get_industry': 'https://api.weixin.qq.com/cgi-bin/template/get_industry',
    # 发送模板信息接口
    'send_templates_message': 'https://api.weixin.qq.com/cgi-bin/message/template/send',
    # 支付下单接口
    'order_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder',
    # jssdk ticket
    'ticket_url': 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=',
}


SCOPE = 'snsapi_userinfo'
PC_LOGIN_SCOPE = 'snsapi_login'
STATE = '1'
LANG = 'zh_CN'
# ----------------------------------------------融云配置---------------------------------------------- #
RONGYUN_Key = 'qf3d5gbjqhy6h'
RONGYUN_Secret = 'r3Kc54N0h1'
