"""
分组管理视图
"""

from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.group_serializers import *
from meiduo_admin.paginations import MyPage


class GroupPermListView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermSimpleModelSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = MyPage
