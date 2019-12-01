import django_filters
from .models import Services,Teachers


class TeachersFilter(django_filters.rest_framework.FilterSet):
    # 以参数的形式筛选，无法满足筛选关联数据的需求
    display = django_filters.CharFilter(field_name='display')
    class Meta:
        model = Teachers
        fields = ('display',)


class ServicesFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Services
        fields = '__all__'
