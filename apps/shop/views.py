from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination # 分页
from rest_framework import filters
from .serializers import *
from .filters import *

from rest_framework.permissions import IsAuthenticated
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, permissions, authentication
from django_filters.rest_framework import DjangoFilterBackend


class ShopPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class CategoryListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    类型
    """
    queryset = Category.objects.all().order_by('-sort')
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    filter_fields = ('status',)


class ShopViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ShopSerializer
    pagination_class = ShopPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.SearchFilter,)
    filter_class = ShopFilter
    filter_fields = ('status', 'teacher')
    search_fields = ['title', 'des', 'mid__nickname']

    def get_queryset(self):
        if self.action == "update" or self.action == "destroy":
            return List.objects.order_by("-id")
        else:
            m = self.request.query_params.get('m', '')
            if m:
                return List.objects.filter(teacher_id=m).order_by("-id")
            else:
                return List.objects.order_by("-id")