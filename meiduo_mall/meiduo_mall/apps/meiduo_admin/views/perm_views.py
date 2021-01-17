"""
权限管理视图
"""
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.perm_serializers import *
from meiduo_admin.paginations import MyPage


# 新建权限可选类型
class ContentTypeListView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeModelSerializer


class PermViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermModelSerializer
    pagination_class = MyPage

    def get_queryset(self):
        return self.queryset.order_by('pk')
