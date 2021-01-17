"""
定义选项表管理的视图
"""
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.option_serializers import *
from meiduo_admin.paginations import MyPage


# 新建选项可选规格
class SpecSimpleListView(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSimpleModelSerializer


class OptionViewSet(ModelViewSet):
    queryset = SpecificationOption.objects.all()
    serializer_class = OptionModelSerializer
    pagination_class = MyPage
