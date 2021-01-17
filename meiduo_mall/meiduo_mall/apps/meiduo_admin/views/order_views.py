# from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from meiduo_admin.serializers.order_serializers import *
from meiduo_admin.paginations import MyPage


class OrderView(UpdateModelMixin, ReadOnlyModelViewSet):
    queryset = OrderInfo.objects.all()
    # 默认序列化器是简单序列化，作用于self.list接口
    serializer_class = OrderSimpleModelSerializer
    pagination_class = MyPage

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return self.queryset.filter(order_id__contains=keyword)
        return self.queryset.all()

    # self.list接口应当使用简单序列化器
    # self.retrieve接口应当使用详情序列化器
    # 总结：同一个视图类中，如何在不同的接口中使用不同的序列化器来实现
    # 构建不同的序列化结果
    def get_serializer_class(self):
        # 如果请求对应的视图函数是list，使用OrderSimpleModelSerializer
        # 如果请求对应的视图函数是retrieve，使用OrderDetailModelSerializer
        # 总结：如何判断此次请求对应的视图函数？
        # 答：self.action = "视图函数名称"
        if self.action == "list":
            return OrderSimpleModelSerializer
        if self.action == "retrieve":
            return OrderDetailModelSerializer
        if self.action == 'partial_update':
            return OrderSimpleModelSerializer

        return self.serializer_class

    # def get_serializer(self, *args, **kwargs): 获取序列化器对象
    # def get_serializer_class(self): 使用哪个序列化器类
