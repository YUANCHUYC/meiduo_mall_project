"""
管理员管理视图
"""
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.admin_serializers import *
from meiduo_admin.paginations import MyPage


# 新建用户可选分组
class AdminGroupListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = AdminGroupModelSerializer


class AdminViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminModelSerializer
    pagination_class = MyPage
