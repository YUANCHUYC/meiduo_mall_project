"""
spu管理的视图
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.spu_serializers import *
from meiduo_admin.paginations import MyPage


# SPU管理
class SPUModelView(ModelViewSet):
    queryset = SPU.objects.all()
    serializer_class = SPUModelSerializer

    pagination_class = MyPage

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.filter(
                name__contains=keyword
            )
        return self.queryset.all()


# 新建SPU可选品牌
class BrandSimpleView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSimpleModelSerializer


class CateSimpleListView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = CateSimpleModelSerializer

    def get_queryset(self):
        parent_id = self.kwargs.get('pk')  # 路径中的pk是父级id

        if parent_id:
            # 如果当前请求是获取二级或三级分类，返回二级或三级分类查询集
            return self.queryset.filter(parent_id=parent_id)
        else:
            # 如果当前请求是获取一级分类，返回一级分类查询集
            return self.queryset.filter(parent=None)


