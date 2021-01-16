from rest_framework.generics import ListAPIView, CreateAPIView
from users.models import User
from meiduo_admin.serializers.user_serializers import UserModelSerializer
from meiduo_admin.paginations import MyPage


class UserView(ListAPIView, CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    pagination_class = MyPage  # 指定分页器

    # 根据查询字符串参数keyword过滤
    def get_queryset(self):
        # 1、获取查询字符串参数keyword --> request.query_params.get("keyword")
        # 如何在非视图函数中获取请求对象；
        # 答：self.request就是请求对象。
        keyword = self.request.query_params.get('keyword')
        # 2、过滤
        if keyword:
            return self.queryset.filter(username__contains=keyword)
        else:
            return self.queryset.all()
