from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination # 分页
from rest_framework import filters
from .serializers import JifenSerializer,JifenAddSerializer
from .models import Jifen

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, authentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

# Create your views here.


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class JifenViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    # 提交评论
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    serializer_class = JifenSerializer
    pagination_class = CommonPagination

    def get_serializer_class(self):
        if self.action == "create":
            return JifenAddSerializer
        return JifenSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Jifen.objects.filter(member_id=user).order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            cash = float('0')
            serializer = self.get_serializer(page, many=True)
            for key, value in enumerate(serializer.data):
                if serializer.data[key]['plus'] == '1':
                    cash = cash + float(serializer.data[key]['jifen'])
                elif serializer.data[key]['plus'] == '2':
                    cash = cash - float(serializer.data[key]['jifen'])
                else:
                    cash = cash + float('0')
            result = {'cash': abs(cash), 'data': serializer.data}
            return self.get_paginated_response(result)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)