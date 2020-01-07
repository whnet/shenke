from django.views.generic import View
from django.http import HttpResponse, HttpResponseServerError
import json
from django.db.models import Q

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework import mixins
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model

User = get_user_model()
from apps.orders.models import Orders
from apps.wechat.serializers import WechatNotifySerializer

from rest_framework.views import APIView
from rest_framework.permissions import *
# 设置解析器 https://www.django-rest-framework.org/api-guide/parsers/
from rest_framework_xml.parsers import *

from apps.utils.WechatAPI import *
from apps.user.serializers import *
from rest_framework.authentication import SessionAuthentication
from apps.utils.permissions import IsOwnerOrReadOnly
from apps.utils import Config
from django.core.cache import cache


class WechatNotifyViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Orders.objects.all()
    serializer_class = WechatNotifySerializer


class WechatPaymentXMLParser(XMLParser):
    media_type = 'text/xml'


class WechatNotifyView(APIView):
    """
    微信回调接口
    """
    authentication_classes = []
    permission_classes = (AllowAny,)
    parser_classes = (WechatPaymentXMLParser,) # 设置解析器 https://www.django-rest-framework.org/api-guide/parsers/

    def post(self, request):
        data = request.data
        out_trade_no = data['out_trade_no']
        # 根据 out_trade_no 更新数据库
        if data['result_code'] == 'SUCCESS':
            order = Orders.objects.get(out_trade_no=out_trade_no,status='0')
            # 支付成功后 判断是否要生成另外两个相同的订单，状态为支付，并标记为 taocan 为1
            if order.belong != '0' and order.status=='0':
                count = 0
                while True:
                    count = count + 1
                    order_add = Orders()
                    order_add.title = order.title + '套餐' + str(count+1)
                    order_add.price = order.price
                    order_add.type = order.type
                    order_add.out_trade_no = order.out_trade_no
                    order_add.belong = order.belong
                    order_add.status = 1
                    order_add.detail = order.detail
                    order_add.taocan = count+1
                    order_add.kaiqi = 2
                    order_add.comments = order.comments
                    order_add.mid_id = order.mid_id
                    order_add.teacher_id = order.teacher_id
                    order_add.tomember_id = order.tomember_id
                    order_add.pid = order.pid
                    order_add.save()
                    if count == 2:
                        order.status = 1
                        order.taocan = 1
                        order.title = order.title + '套餐1'
                        order.save()
                        break
            else:
                order.status = 1
                order.save()
            # 支付成功后 生成另外两个相同的订单，状态为支付 END
            # 可以选择这里实现订单成功后发送模板消息，给老师去发送
            '''
            首先要判断是否关注了公众号
            第一步：获取模版ID
            第二步：请求接口 POST请求 https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
            文档如下：https://mp.weixin.qq.com/advanced/tmplmsg?action=faq&token=19356833&lang=zh_CN
            '''
            ACCESS_TOKEN = cache.get('access_token')
            # 老师公众号收到提醒
            teacher = UserProfile.objects.get(pk=order.tomember_id)
            getInfoRequest = requests.get('https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (ACCESS_TOKEN, teacher.openid))
            subscribe = json.loads(getInfoRequest.text)['subscribe']
            if subscribe == 1:
                datas = {
                    "touser": '',
                    "template_id": "0V16YmAZ-8_04rxp92bPkRtcwgeVnjv8MdbGAShhbro",
                    "url": "",
                    "topcolor": "#FF0000",
                    "data": {
                        "first": {
                            "value": "感谢您选择菩提树，客户刚预约了您的服务，请尽快【接单】。72小时未回复系统自动退款。",
                            "color": "#173177"
                        },
                        "keyword1": {
                            "value": '',
                            "color": "#173177"
                        },
                        "keyword2": {
                            "value": '',
                            "color": "#173177"
                        },
                        "remark": {
                            "value": "点击这里进入订单页",
                            "color": "#ef0606"
                        },
                    }
                }
                pass
                datas['touser'] = teacher.openid
                datas['url'] = 'http://vip.putishu.ren/#/myordertaking'
                datas['data']['keyword1']['value'] = order.title
                datas['data']['keyword2']['value'] = time.strftime("%Y-%m-%d", time.localtime())
                content = json.dumps(datas)
                result1 = requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (ACCESS_TOKEN), content)
            # 客户公众号收到提醒
            user = UserProfile.objects.get(pk=order.mid_id)
            getInfoRequest = requests.get(
                'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
                ACCESS_TOKEN, user.openid))
            subscribeUser = json.loads(getInfoRequest.text)['subscribe']
            if subscribeUser == 1:
                datas = {
                    "touser": '',
                    "template_id": "0V16YmAZ-8_04rxp92bPkRtcwgeVnjv8MdbGAShhbro",
                    "url": "",
                    "topcolor": "#FF0000",
                    "data": {
                        "first": {
                            "value": "感谢您选择菩提树，老师正在接单的路上，请耐心等待如72小时未回复会原路退款",
                            "color": "#173177"
                        },
                        "keyword1": {
                            "value": '',
                            "color": "#173177"
                        },
                        "keyword2": {
                            "value": '',
                            "color": "#173177"
                        },
                        "remark": {
                            "value": "如有疑问，请公众号中回复关键词“客服”，联系客服。点击这里进入订单页",
                            "color": "#173177"
                        },
                    }
                }
                pass
                datas['touser'] = user.openid
                datas['url'] = 'http://vip.putishu.ren/#/myorders'
                datas['data']['keyword1']['value'] = order.title
                datas['data']['keyword2']['value'] = time.strftime("%Y-%m-%d", time.localtime())
                content = json.dumps(datas)
                result2 = requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (ACCESS_TOKEN), content)
            # 响应微信的请求
            resp = '''
            <xml>
              <return_code><![CDATA[SUCCESS]]></return_code>
              <return_msg><![CDATA[OK]]></return_msg>
            </xml>
            '''
            return HttpResponse(resp, content_type="text/xml")
        else:
            resp = {'msg': 'error'}
            return HttpResponse(json.dumps(resp), content_type="application/json")


class WechatViewSet(View):
    wechat_api = WechatLogin()


class AuthView(WechatViewSet):
    # 这里返回授权登录的链接，前端跳转去授权 url在微信客户端打开就能看到返回的code值
    def get(self, request):
        url = self.wechat_api.get_code_url()
        resp = {'msg': 100, 'url': url}
        return HttpResponse(json.dumps(resp), content_type="application/json")


class JssdkViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # 验证权限，这里只认证session，如果使用
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        ticket = JssdkAPI.get_ticket(self)
        url = request.data['url']
        result = Sign.sign(self,ticket,url)

        resp = {'msg': 100, 'result': result}
        return HttpResponse(json.dumps(resp), content_type="application/json")


class OauthInfoView(WechatViewSet):

    def get(self, request):
        if 'code' in request.GET:
            code = request.GET['code']
            access_token, openid = self.wechat_api.get_oauth_access_token(code)
            if access_token is None or openid is None:
                return HttpResponseServerError('get code error')
            user_info, error = self.wechat_api.get_user_info(access_token, openid)
            if error:
                return HttpResponseServerError('get access_token error')

            user = User.objects.all().filter(openid=user_info['openid']).values('id','update_status')
            nickname = user_info['nickname'].encode('iso8859-1').decode('utf-8'),
            if user.count() == 0:
                # 数据库中没有数据，这次获取数据从user_info中得到
                shareopenid = request.GET['shareopenid']
                sharetime = request.GET['sharetime']
                shareurl = request.GET['shareurl']
                userCreate = User.objects.create(
                  nickname=nickname[0],
                  username=user_info['openid'],
                  avatar=user_info['headimgurl'],
                  openid=user_info['openid'],
                  upto=shareopenid,
                  sharetime=sharetime,
                  shareurl=shareurl,
                  bindtime=int(time.time()),
                )
                re_dict = {}
                payload = jwt_payload_handler(userCreate)
                re_dict["mid"] = user[0]['id']
                re_dict["avatar"] = user_info['headimgurl']
                re_dict["openid"] = user_info['openid']
                re_dict["token"] = jwt_encode_handler(payload)
                resp = {'msg': 100, 'result': re_dict}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            else:
                # 更新
                userInfo = User.objects.get(openid=user_info['openid'])
                if user[0]['update_status'] == '0':
                    avatar = user_info['headimgurl']
                    User.objects.filter(openid=user_info['openid']).update(
                        nickname= nickname[0],
                        avatar= avatar,)

                re_dict = {}
                payload = jwt_payload_handler(userInfo)
                re_dict["mid"] = user[0]['id']
                re_dict["avatar"] = user_info['headimgurl']
                re_dict["openid"] = user_info['openid']
                re_dict["token"] = jwt_encode_handler(payload)
                resp = {'msg': 100, 'result': re_dict}
                return HttpResponse(json.dumps(resp), content_type="application/json")


class OrderPayViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Orders.objects.all()

    def create(self, request, *args, **kwargs):
        upto = self.request.user.upto
        if 'price' in request.data:
            rand = random.randint(1000, 999999)
            out_trade_no = ''.join(random.sample(string.ascii_letters + string.digits, 10)) + str(rand)
            total_fee = int(float(request.data['price']) * 100)
            spbill_create_ip = request.META['REMOTE_ADDR']
            openid = request.data['openid']
            if total_fee != 0:
                # return HttpResponse(openid, content_type="application/json")
                # notify_url = 'https://cx.emituo.top/wechatnotify/'
                notify_url = Config.Notify_url
                WechatOrders = WechatOrder(
                                    body=request.data['title'],
                                    trade_type='JSAPI',
                                    out_trade_no=out_trade_no,
                                    openid= openid,
                                    total_fee=total_fee,
                                    spbill_create_ip=spbill_create_ip,
                                    notify_url=notify_url)
                datas, error = WechatOrders.order_post()
                if error:
                    return HttpResponse(json.dumps({'msg': error}), content_type="application/json")

                order_data = datas['prepay_id'].encode('iso8859-1').decode('utf-8'),
                pay = WechatPayAPI(package=order_data[0])
                dic = pay.get_dic()
                dic["package"] = "prepay_id=" + order_data[0]
            else:
                dic = []

            # 查询用户信息
            userInfo = UserProfile.objects.get(openid=openid)
            if request.data['type'] == 'teacher':
                tid = request.data['tid']
            elif request.data['type'] == 'guangyiguang':
                tid = request.data['tid']
            else:
                return HttpResponse('error', content_type="application/json")

            # 写入orders_orders数据库
            Orders.objects.create(
                                title= request.data['title'],
                                  price= request.data['price'],
                                  detail= request.data['detail'],
                                  belong= request.data['belong'],
                                  mid_id = userInfo.id,
                                  upto = upto,
                                  kaiqi = 1,
                                  tomember_id = request.data['tomember_id'],
                                  status = 0 if total_fee != 0 else 1, # 1为已付款状态和待接单的状态
                                  teacher_id = tid,
                                  type = request.data['type'],
                                  pid = request.data['pid'],
                                  out_trade_no= out_trade_no,
                                  )
            return HttpResponse(json.dumps(dic), content_type="application/json")
        else:
            dic = request.data['price']
            return HttpResponse(json.dumps(dic), content_type="application/json")



