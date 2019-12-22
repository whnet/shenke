import django_filters
from .models import Services,Teachers


class TeachersFilter(django_filters.rest_framework.FilterSet):
    # 以参数的形式筛选，无法满足筛选关联数据的需求
    class Meta:
        model = Teachers
        fields = '__all__'


class ServicesFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Services
        fields = '__all__'
