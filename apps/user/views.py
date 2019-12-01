from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse
import json,requests,time

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, permissions, authentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework.response import Response
from rest_framework import viewsets, status

from rest_framework.permissions import *
from apps.utils.permissions import IsOwnerOrReadOnly

# 融云
from apps.utils.rongyun.User import RongyunUser
# 七牛云
from qiniu import Auth
from qiniu import BucketManager
from utils import Config
from django.core.cache import cache

from apps.user.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination # 分页
from apps.orders.models import Orders

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | Q(mobile=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserDetailSerializer
        elif self.action == "update":
            return UserUpdateSerializer

        return UserDetailSerializer

    def get_permissions(self):
        # action 属性只有使用 viewset 的时候才存在
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.nickname if user.nickname else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写该方法，不管传什么id，都只返回当前用户,这个和RetrieveModelMixin对应，注意deleMixi也有这个方法
    # def get_object(self):
    #     return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class SharePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class ShareViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    pagination_class = SharePagination
    serializer_class = UserShareSerializer

    def get_queryset(self):
        test = time.strftime("%Y-%m-%d", time.localtime())
        user = self.request.user.openid
        return User.objects.filter(upto=user).order_by("-id")


class UserDetailViewSet(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ZiliaoSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class RongyunViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def create(self, request, *args, **kwargs):
        userId = request.data['userId']
        userName = request.data['userName']
        portraitUri = request.data['avatar']
        rongyun = RongyunUser()
        chatUser = rongyun.getToken(userId, userName, portraitUri)

        return HttpResponse(json.dumps(chatUser.result), content_type="application/json")


class DownRongyunViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    authentication_classes = ([])
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        userId = request.data['userId']
        userName = request.data['userName']
        portraitUri = request.data['avatar']
        rongyun = RongyunUser()
        chatUser = rongyun.getToken(userId, userName, portraitUri)

        return HttpResponse(json.dumps(chatUser.result), content_type="application/json")


class QiniuViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        bucket_name = 'shenduce'
        q = Auth(Config.QINIU_Ak, Config.QINIU_Sk)
        bucket = BucketManager(q)
        if cache.has_key('access_token'):
            access_token = cache.get('access_token')
            media_id = self.request.data['media_id']
            url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token={}&media_id={}'.format(access_token,media_id)
            ret, info = bucket.fetch(url, bucket_name)
            return HttpResponse(json.dumps(ret), content_type="application/json")
        else:
            return HttpResponse(json.dumps(['error']), content_type="application/json")


class QiniutestViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        access_key = Config.QINIU_Ak
        secret_key = Config.QINIU_Sk
        qiniu = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'shenduce'
        # 上传后保存的文件名，前后台应该一致，否则出现key doesn't match scope，这里设置为None
        key = None
        result = qiniu.upload_token(bucket_name, key, 360)

        return HttpResponse(json.dumps(result), content_type="application/json")