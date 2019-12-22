from rest_framework.pagination import PageNumberPagination # 分页
from rest_framework import viewsets
from rest_framework import filters
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, authentication

# 用户权限控制
from rest_framework.permissions import IsAuthenticated
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GridPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class TeacherViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    #filter() 等方法中的关键字参数查询都是一起进行“AND” 的。 如果你需要执行更复杂的查询（例如OR 语句），你可以使用Q 对象。
    # queryset = Teachers.objects.all().filter(~Q(status=2)).order_by("-id")

    # 状态为通过 且 服务项目不能为空的 才在前台显示
    queryset = Teachers.objects.filter(status=1).order_by("-id")
    pagination_class = CommonPagination  # 分页
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 排序 rank 人气榜（感谢数/总已完成订单数） rec_status 热推榜(rec字段--置顶状态) uptated 新晋榜
    ordering_fields = ('updated', 'haopinglv', 'price')
    filter_fields = ('type', 'mid_id')
    # 搜索 在search_fields中加入一个外键的名字是不能查询的,要写成(外键名__外键中的字段名)的形式.
    search_fields = ['experience', 'realname', 'honor', 'resume', 'type__title', 'mid__nickname']

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return TeacherDetailSerializer
        return TeacherSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        list = []
        m = self.request.query_params.get('m', '')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for key,value in enumerate(serializer.data):
                if m == 'rec':
                    if value['data']['services_count'] and value['rec'] == '1':
                        list.append(serializer.data[key])
                else:
                    if serializer.data[key]['data']['services_count']:
                        list.append(serializer.data[key])
            return self.get_paginated_response(list)

        serializer = self.get_serializer(queryset, many=True)
        for key, value in enumerate(serializer.data):
            if serializer.data[key]['data']['services_count']:
                list.append(serializer.data[key])
        return Response(list)


class UpdateTeacherViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 如果一个老师先添加了服务项目，后又删除了所有的项目，会导致前台仍然能看到，需要根据服务项目进行筛选
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user.id
        return Teachers.objects.filter(mid=user)

    def get_serializer_class(self):
        return UpdateTeacherSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'category' in self.request.data:
            category = self.request.data['category']
            if category:
                # 保存主表信息后 删除原来所有的信息 id指category表中的ID add(name) remove(name) clear()
                teacher = serializer.save()
                teacher.type.clear()
                for data in category:
                    name = Categories.objects.get(id=data)
                    teacher.type.add(name)
                serializer.save()
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        # 为真时的结果 if 判定条件 else 为假时的结果
        if 'category' in self.request.data:
            category = self.request.data['category']
            if category:
                # 保存主表信息后 删除原来所有的信息 id指category表中的ID add(name) remove(name) clear()
                teacher = serializer.save()
                teacher.type.clear()
                for data in category:
                    name = Categories.objects.get(id=data)
                    teacher.type.add(name)
                serializer.save()


class CategoryViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    老师的分类
    """
    queryset = Categories.objects.all().order_by("-sort")
    serializer_class = CategoriesSerializer


class ServiceViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ServicesSerializer

    def get_queryset(self):
        if self.action == "update" or self.action == "destroy":
            return Services.objects.order_by("-id")
        else:
            m = self.request.query_params.get('m', '')
            if m:
                return Services.objects.filter(tid_id=m).order_by("-id")
            else:
                return Services.objects.order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if self.request.query_params.get('page', ''):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    pagination_class = CommonPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tid', )

    # 设置套餐后，将它的sort 设置成1，根据belong更新
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 更新宿主订单
        belong = request.data['belong']
        if belong:
            Services.objects.filter(id=belong).update(sort=1,)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
