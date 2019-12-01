from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination # 分页
from rest_framework import filters
from .serializers import *
from .filters import *

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, permissions, authentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class OrdersPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class OrdersListViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    订单列表,根据会员性质分为，我的订单（根据mid查找）；接单（根据teacher查找）
    """
    # 订单的身份验证
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    serializer_class = OrdersSerializer
    queryset = Orders.objects.all().order_by("-id")
    pagination_class = OrdersPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('title',)
    filter_fields = ('teacher', 'mid', 'status')


class ChatViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    serializer_class = ChatSerializer
    queryset = Orders.objects.all().order_by("-id")


class CommentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    # 提交评论
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    serializer_class = CommentSerializer
    queryset = Orders.objects.all().order_by("-id")


class CommentsViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    # 首页评论列表及详情，控制显示的个数，使用切片
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # 首页显示10条最新的五星好评，超过20字显示，10位要不一样的老师
    serializer_class = CommentsSerializer

    pk_list = []
    teacher_list = []
    comments = Orders.objects.all().order_by("created")
    # 判断数据库是否存在，如果不存在就不执行，否则会报数据库不存在
    if 1 == 1:
        for item in comments:
            ganxie = item.ganxie
            comment = item.comments
            if len(comment) > 20 and ganxie == '1':
                pk_list.append(item.id)
                teacher_list.append(item.teacher_id)
    # 去除重复的值，显示10位不同的老师
    dict = dict(zip(teacher_list,pk_list))
    new_list = list(dict.values())
    new_pk_list = new_list[::-1]
    queryset = Orders.objects.filter(pk__in=new_pk_list).order_by("-created")[:10]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_fields = ('id', 'teacher', 'type', 'service')


class CommentdetailViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    # 详情页的评论列表及详情，控制显示的个数，使用切片
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = CommentsSerializer
    pk_list = []
    comments = Orders.objects.all().order_by("created")
    # 判断数据库是否存在，如果不存在就不执行，否则会报数据库不存在
    for item in comments:
        ganxie = item.ganxie
        comment = item.comments
        # filter() 不能再使用切片，通过这种方法实现限制条数
        if len(comment) > 0 and len(pk_list) <= 5:
            pk_list.append(item.id)
    queryset = Orders.objects.filter(pk__in = pk_list).order_by("-created")
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('teacher','type','pid')


class AllViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    # 还不会获得参数，先这样写，全部评论需要使用分页功能，单独独立吧。
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = CommentsSerializer
    pk_list = []
    comments = Orders.objects.all().order_by("created")
    # 判断数据库是否存在，如果不存在就不执行，否则会报数据库不存在
    for item in comments:
        comment = item.comments
        # filter() 不能再使用切片，通过这种方法实现限制条数
        if len(comment) > 0:
            pk_list.append(item.id)
    queryset = Orders.objects.filter(pk__in = pk_list).order_by("-created")
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('teacher','type','pid')