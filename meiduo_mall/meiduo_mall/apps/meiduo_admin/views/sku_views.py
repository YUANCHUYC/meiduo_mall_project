"""
针对sku管理的视图
"""
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.sku_serializers import *
from meiduo_admin.paginations import MyPage
from django.db.models import Q


class SKUGoodsView(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer

    pagination_class = MyPage

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        return self.queryset.all()


# 新建SKU可选三级分类序列化返回视图
class SKUGoodsCateView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = SKUGoodsCateModelSerializer

    def get_queryset(self):
        return self.queryset.filter(
            parent_id__gt=37  # 父级的id大于37的是三级分类
        )


# 新建SKU可选SPU列表数据视图
class SPUSimpleView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleModelSerializer


# 用户选择spu关联的规格列表数据视图
class SpecOptView(ListAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSimpleModelSerializer

    # 根据路径中的spu_id过滤出规格查询集
    def get_queryset(self):
        # 路径参数pk，就是spu的id值
        # 如何在非视图函数中，获取路径参数？！
        # 答：self.kwargs封装了路径参数(字典)
        # self.kwargs = {"pk": 2}
        spu_id = self.kwargs.get('pk')
        return self.queryset.filter(
            spu_id=spu_id
        )
