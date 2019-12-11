from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from .serializers import *
from .filters import *
import time,requests,json,os,xmltodict
from django.core.cache import cache
from django.db.models import Q
import random,hashlib,string,datetime
from apps.utils import Config


from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, authentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import *
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class NotifyWechatViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = ChatSerializer
    queryset = Orders.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        '''
        首先要判断是否关注了公众号
        第一步：获取模版ID
        第二步：请求接口 POST请求 https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
        文档如下：https://mp.weixin.qq.com/advanced/tmplmsg?action=faq&token=19356833&lang=zh_CN
        '''
        # 老师已经接单了，请点击这里和老师沟通吧！
        ACCESS_TOKEN = cache.get('access_token')
        type = self.request.data['type']
        TITLE = self.request.data['title']
        OPENID = self.request.data['openid']
        URL = self.request.data['url']
        getInfoRequest = requests.get(
            'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
                ACCESS_TOKEN, OPENID))
        subscribe = json.loads(getInfoRequest.text)['subscribe']
        if subscribe == 1:
            if type == 'start':
                datas = {
                    "touser": '',
                    "template_id": "EnDnS7Sm4a1eVMQ3bkqWit0jN8iN_nOIFbGagKaN5Pc",
                    "url": '',
                    "topcolor": "#FF0000",
                    "data": {
                        "first": {
                            "value": "老师已经接单了，请点击这里和老师沟通吧！",
                            "color": "#173177"
                        },
                        "keyword1": {
                            "value": "",
                            "color": "#173177"
                        },
                        "keyword2": {
                            "value": "",
                            "color": "#173177"
                        },
                        "remark": {
                            "value": "如有疑问，请公众号中回复关键词“客服”，联系客服。",
                            "color": "#173177"
                        },
                    }
                }
                pass
                datas['touser'] = OPENID
                datas['url'] = URL
                datas['data']['keyword1']['value'] = TITLE
                datas['data']['keyword2']['value'] = '已接单'
                content = json.dumps(datas)
                requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (ACCESS_TOKEN), content)
            elif type == 'end':
                datas = {
                    "touser": '',
                    "template_id": "EnDnS7Sm4a1eVMQ3bkqWit0jN8iN_nOIFbGagKaN5Pc",
                    "url": '',
                    "topcolor": "#FF0000",
                    "data": {
                        "first": {
                            "value": "老师已经结束服务了，请点击这里对老师的服务做评价吧！",
                            "color": "#173177"
                        },
                        "keyword1": {
                            "value": "",
                            "color": "#173177"
                        },
                        "keyword2": {
                            "value": "",
                            "color": "#173177"
                        },
                        "remark": {
                            "value": "如有疑问，请公众号中回复关键词“客服”，联系客服。",
                            "color": "#173177"
                        },
                    }
                }
                pass
                datas['touser'] = OPENID
                datas['url'] = URL
                datas['data']['keyword1']['value'] = TITLE
                datas['data']['keyword2']['value'] = '待评价'
                content = json.dumps(datas)
                requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (ACCESS_TOKEN),content)
            elif type == 'judan':
                datas = {
                    "touser": '',
                    "template_id": "EnDnS7Sm4a1eVMQ3bkqWit0jN8iN_nOIFbGagKaN5Pc",
                    "url": '',
                    "topcolor": "#FF0000",
                    "data": {
                        "first": {
                            "value": "老师已拒单，费用72小时退款到您微信钱包。可预约其他老师看看哦～",
                            "color": "#173177"
                        },
                        "keyword1": {
                            "value": "",
                            "color": "#173177"
                        },
                        "keyword2": {
                            "value": "",
                            "color": "#173177"
                        },
                        "remark": {
                            "value": "如有疑问，请公众号中回复关键词“客服”，联系客服。",
                            "color": "#173177"
                        },
                    }
                }
                pass
                datas['touser'] = OPENID
                datas['url'] = URL
                datas['data']['keyword1']['value'] = TITLE
                datas['data']['keyword2']['value'] = '已拒单'
                content = json.dumps(datas)
        return Response({'status':200001}, status=status.HTTP_200_OK)


class ShareOrdersListViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    serializer_class = OrdersSerializer

    def get_queryset(self):
        # 状态不能为0，2，6
        return Orders.objects.filter(Q(upto=self.request.user.openid) & ~Q(status=0) & ~Q(status=2) & ~Q(status=6)).order_by("-id")


class OrdersListViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )

    def get_serializer_class(self):
        if self.request.GET.get('sum',''):
            return JifenSerializer
        return OrdersSerializer

    def get_queryset(self):
        user = self.request.user.id
        # 如果status == '-1' ，就是全部的订单，否则就筛选对应，设置区分是我的订单 还是 我要接单 使用 type 区分
        status = self.request.GET.get('status', '')
        type = self.request.GET.get('type', '')
        if status and type:
            if type == 'taking':
                return Orders.objects.filter(tomember_id=user, status=status).order_by("-id")
            elif type == 'buy':
                return Orders.objects.filter(mid_id=user, status=status).order_by("-id")
        elif status == '' and type:
            if type == 'taking':
                return Orders.objects.filter(tomember_id=user).order_by("-id")
            elif type == 'buy':
                return Orders.objects.filter(mid_id=user).order_by("-id")
            elif type == 'jifen':
                return Orders.objects.filter(mid_id=user).order_by("-id")

        return Orders.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IncomeViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    # 订单的身份验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('teacher', 'mid', 'status')

    def get_serializer_class(self):
        if self.request.GET.get('m',''):
            return OrdersSerializer
        return OrdersSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Orders.objects.filter(tomember_id=user).order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            m = self.request.GET.get('m', '')
            serializer = self.get_serializer(page, many=True)
            if m == 'income':
                t = time.time()
                now = int(t)
                list = []
                sum = float(0)
                for key, value in enumerate(serializer.data):
                    dt = serializer.data[key]['created']
                    ts = int(time.mktime(time.strptime(dt, '%Y-%m-%d')))
                    if now - ts > 1 and serializer.data[key]['status'] == '5':
                        sum = sum + float(serializer.data[key]['price'])
                        list.append({'price':serializer.data[key]['price']})
                return self.get_paginated_response({'sum':sum,'list':list})
            elif m == 'pay':
                cash = float('0')
                for key, value in enumerate(serializer.data):
                    if serializer.data[key]['status'] == '2':
                        cash = cash - float(serializer.data[key]['price'])
                    elif serializer.data[key]['status'] == '0' or serializer.data[key]['status'] == '1':
                        cash = cash
                    else:
                        cash = cash + float(serializer.data[key]['price'])

                return self.get_paginated_response({'cash':cash,'list':serializer.data})

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChatViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = ChatSerializer
    queryset = Orders.objects.all().order_by("-id")


class CiciouumlViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ([])
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all().order_by("-id")


class ChatlogsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    # 聊天窗口的身份验证，mixins.ListModelMixin在上线要去掉
    permission_classes = (AllowAny,)
    authentication_classes = ([])
    serializer_class = ChatlogsSerializer
    queryset = Orders.objects.all().order_by("-id")


class CommentsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "update":
            return CommentSerializer
        return CommentsSerializer

    def get_queryset(self):
        # 筛选状态放到 list 方法中 去筛选
        return Orders.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 首页显示感谢，评论超过20字显示，10位要不一样的老师
        serializer = self.get_serializer(queryset, many=True)
        teacher = self.request.GET.get('teacher', '')
        guangyiguang = self.request.GET.get('product', '')
        type = self.request.GET.get('type', '')
        all = self.request.GET.get('all', '')
        list = []
        if teacher and type=='teacher':
            for key, value in enumerate(serializer.data):
                test = value['teacher']['id']
                pid = value['pid']
                if self.statusIsok(value['teacher']['id']) and key < 10 and value['type'] == type\
                        and value['teacher']['id']==int(teacher) and value['status'] == '5':
                    list.append(serializer.data[key])
        elif guangyiguang and type=="product":
            for key, value in enumerate(serializer.data):
                if self.statusIsok(value['teacher']['id']) and key < 10 and value['type'] == type\
                        and value['pid'] == int(guangyiguang)  and value['status'] == '1':
                    list.append(serializer.data[key])
        else:
            for key, value in enumerate(serializer.data):
                if self.statusIsok(value['teacher']['id']) and len(value['comments']) >= 1 \
                        and value['ganxie'] == '1' and key < 10  and value['status'] == '5':
                    list.append(serializer.data[key])

        return Response(list)

    def statusIsok(self,teacher_id):
        teacher = Teachers.objects.get(id=teacher_id)
        status = True if teacher.status == '1' else False
        return status


class WithdrawViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = WithdrawSerializer
    pagination_class = CommonPagination

    def get_queryset(self):
        user = self.request.user.id
        return Withdraw.objects.filter(member_id=user).order_by("-id")


class TuikuanViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # 用户退款，超过72小时，订单为老师未接单（待接单状态），则系统自动退款
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        list = []
        # 退款接口 POST
        UNIFIED_ORDER_URL = 'https://api.mch.weixin.qq.com/secapi/pay/refund'

        # 1 配置证书文件路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ssh_keys_path = os.path.join(BASE_DIR, 'd2p3/cert')
        certpem = os.path.join(ssh_keys_path, "apiclient_cert.pem")
        keypem = os.path.join(ssh_keys_path, "apiclient_key.pem")

        for key, value in enumerate(serializer.data):
            created = value['created']
            timeArray = time.strptime(created, "%Y-%m-%d")
            order_created = int(time.mktime(timeArray))
            now = int(time.time())
            expiretime = now - order_created > 2
            if expiretime and value['status'] == '1':
                nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                out_trade_no = value['out_trade_no']
                out_refund_no = value['out_trade_no']
                notify_url = ''
                total_fee = int(float(value['price']) * 100)
                refund_fee = int(float(value['price']) * 100)
                # 2 配置请求参数 第一步：对参数按照key=value的格式，并按照参数名ASCII字典序排序如下：
                stringA = "appid={}&mch_id={}&nonce_str={}&out_refund_no={}&out_trade_no={}&refund_fee={}&total_fee={}".format(
                    Config.APPID, Config.MCH_ID, nonce_str, out_refund_no, out_trade_no, refund_fee, total_fee)
                # 第二步：拼接API密钥：
                stringSignTemp = stringA + "&key={}".format(Config.API_KEY)  # 注：key为商户平台设置的密钥key
                sign = hashlib.md5(stringSignTemp.encode(encoding='utf-8')).hexdigest().upper()
                # 3 配置 XML
                xml = "<xml>" \
                      "<appid><![CDATA[{}]]></appid>" \
                      "<mch_id><![CDATA[{}]]></mch_id>" \
                      "<out_trade_no><![CDATA[{}]]></out_trade_no>" \
                      "<out_refund_no><![CDATA[{}]]></out_refund_no>" \
                      "<total_fee><![CDATA[{}]]></total_fee>" \
                      "<refund_fee><![CDATA[{}]]></refund_fee>" \
                      "<notify_url><![CDATA[{}]]></notify_url>" \
                      "<nonce_str><![CDATA[{}]]></nonce_str>" \
                      "<sign><![CDATA[{}]]></sign>" \
                      "</xml>".format(Config.APPID, Config.MCH_ID, out_trade_no, out_refund_no, total_fee, refund_fee,
                                      notify_url, nonce_str, sign)
                # res = requests.post(UNIFIED_ORDER_URL, cert=(certpem, keypem), data=xml.encode('utf-8'))
                # text = str(res.content,encoding='utf-8')
        return Response(list)


class JiekuanViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # 老师结款
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = WithdrawSerializer
    queryset = Withdraw.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        list = []
        # 打款接口 POST
        UNIFIED_ORDER_URL = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers'

        # 1 配置证书文件路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ssh_keys_path = os.path.join(BASE_DIR, 'd2p3/cert')
        certpem = os.path.join(ssh_keys_path, "apiclient_cert.pem")
        keypem = os.path.join(ssh_keys_path, "apiclient_key.pem")
        for key, value in enumerate(serializer.data):
            nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
            partner_trade_no = ''.join(random.sample(string.ascii_letters + string.digits, 22))
            openid = value['openid']
            check_name = 'NO_CHECK'
            amount = int(float(value['price']) * 100)
            desc = '{}提现成功'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.META.get("REMOTE_ADDR")
            spbill_create_ip = ip
            # 2 配置请求参数 第一步：对参数按照key=value的格式，并按照参数名ASCII字典序排序如下：
            stringA = "amount={}&check_name=NO_CHECK&desc={}&mch_appid={}&mchid={}" \
                      "&nonce_str={}&openid={}&partner_trade_no={}&spbill_create_ip={}".format(
                amount, desc, Config.APPID, Config.MCH_ID, nonce_str, openid, partner_trade_no, spbill_create_ip)
            # 第二步：拼接API密钥：
            stringSignTemp = stringA + "&key={}".format(Config.API_KEY)  # 注：key为商户平台设置的密钥key
            sign = hashlib.md5(stringSignTemp.encode(encoding='utf-8')).hexdigest().upper()
            # 3 配置 XML
            xml = "<xml>" \
                  "<mch_appid><![CDATA[{}]]></mch_appid>" \
                  "<mchid><![CDATA[{}]]></mchid>" \
                  "<nonce_str><![CDATA[{}]]></nonce_str>" \
                  "<partner_trade_no><![CDATA[{}]]></partner_trade_no>" \
                  "<openid><![CDATA[{}]]></openid>" \
                  "<check_name><![CDATA[{}]]></check_name>" \
                  "<amount><![CDATA[{}]]></amount>" \
                  "<desc><![CDATA[{}]]></desc>" \
                  "<spbill_create_ip><![CDATA[{}]]></spbill_create_ip>" \
                  "<sign><![CDATA[{}]]></sign>" \
                  "</xml>".format(Config.APPID, Config.MCH_ID, nonce_str, partner_trade_no,
                                  openid, check_name, amount, desc, spbill_create_ip, sign)
            res = requests.post(UNIFIED_ORDER_URL, cert=(certpem, keypem), data=xml.encode('utf-8'))
            dict = xmltodict.parse(res.text)
            return_code = dict['xml']['return_code']
            result_code = dict['xml']['result_code']
            if return_code == 'SUCCESS' and result_code == 'SUCCESS':
                partner_trade_no = dict['xml']['partner_trade_no']
                payment_no = dict['xml']['payment_no']
                payment_time = dict['xml']['payment_time']
                Withdraw.objects.filter(id=8).update(
                    partner_trade_no=partner_trade_no,
                    payment_no=payment_no,
                    status=1,
                    payment_time=payment_time, )
            text = str(res.content, encoding='utf-8')
        return Response(list)