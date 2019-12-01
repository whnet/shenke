"""d2p3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token


import xadmin
from apps.ads.views import AdsListViewSet
from apps.managefiles.views import UploadViewSet,UploadShopViewSet
from apps.orders.views import CommentsViewSet
from apps.orders.views import *
from apps.shop.views import ShopViewSet, CategoryListViewSet
from apps.teacher.views import TeacherViewSet, CategoryViewSet, ServiceViewSet,UpdateTeacherViewSet
from apps.user.views import *
from apps.wechat.views import *
from apps.jifen.views import JifenViewSet
from .settings import MEDIA_ROOT

router = routers.DefaultRouter()
# 会员管理 base_name:   用来生成urls名字，如果viewset中没有包含queryset, base_name一定要有

# 老师管理
router.register(r'teacher', TeacherViewSet, base_name='teacher')
router.register(r'updateteacher', UpdateTeacherViewSet, base_name='updateteacher')
router.register(r'catogary', CategoryViewSet, base_name='catogary')

# 广告管理
router.register(r'advertisement', AdsListViewSet, base_name='advertisement')

# 逛逛管理
router.register(r'shop', ShopViewSet, base_name='shop')
router.register(r'shoptags', CategoryListViewSet, base_name='shoptags')

# 融云token
router.register(r'rongyun', RongyunViewSet, base_name='rongyun')
router.register(r'downrongyun', DownRongyunViewSet, base_name='downrongyun')
# 七牛云token
router.register(r'qiniu', QiniuViewSet, base_name='qiniu')

# 配置register的url
router.register(r'register', UserViewSet, base_name='register')

# 配置users的url, 可以获得指定ID的用户信息
router.register(r'users', UserViewSet, base_name='users')
router.register(r'ziliao', UserDetailViewSet, base_name='ziliao')
# 账单退款、打款操作
router.register(r'tuikuan', TuikuanViewSet, base_name='tuikuan')
router.register(r'dakuan', JiekuanViewSet, base_name='dakuan')


# 配置微信支付接口
router.register(r'wechatpay', OrderPayViewSet, base_name='wechatpay')
# 微信分享接口 使用post 做验证
router.register(r'jssdk', JssdkViewSet, base_name='jssdk')
# 分享推广的数据
router.register(r'share', ShareViewSet, base_name='share')
router.register(r'shareorder', ShareOrdersListViewSet, base_name='shareorder')
# 公众号通知
router.register(r'notifyWechat', NotifyWechatViewSet, base_name='notifyWechat')


# 订单管理
router.register(r'orders', OrdersListViewSet, base_name='orders')
router.register(r'ciciouuml', CiciouumlViewSet, base_name='ciciouuml')
# 收入管理
router.register(r'income', IncomeViewSet, base_name='income')
router.register(r'withdraw', WithdrawViewSet, base_name='withdraw')
# 积分管理
router.register(r'jifen', JifenViewSet, base_name='jifen')

# 聊天管理
router.register(r'chat', ChatViewSet, base_name='chat')
router.register(r'chatlogs', ChatlogsViewSet, base_name='chatlogs')

# 服务项目
router.register(r'service', ServiceViewSet, base_name='service')

router.register(r'upload', UploadViewSet, base_name='upload')
router.register(r'upg', UploadShopViewSet, base_name='upg')

# 订单&评论
router.register(r'comments', CommentsViewSet, base_name='comments')


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path('^', include(router.urls)),
    # 静态文件
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 富文本编辑器
    path('ueditor/', include('DjangoUeditor.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # 生成API文档
    path('docs/', include_docs_urls(title='API文档')),
    # drf自带的token授权登录,获取token需要向该地址post数据
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的token认证，这里得到的token，添加到header中，从而进行验证
    path('login/', obtain_jwt_token),
    # 微信授权登录
    path('auth/', AuthView.as_view()),
    path('wechatnotify/', WechatNotifyView.as_view()),
    # 微信授权得到用户信息
    path('info/', OauthInfoView.as_view()),
]
