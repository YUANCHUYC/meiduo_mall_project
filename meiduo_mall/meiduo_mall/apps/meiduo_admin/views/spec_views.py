"""
定义规格管理的视图
"""

from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.spec_serializers import *
from meiduo_admin.paginations import MyPage


class SpecViewSet(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecModelSerializer
    pagination_class = MyPage
