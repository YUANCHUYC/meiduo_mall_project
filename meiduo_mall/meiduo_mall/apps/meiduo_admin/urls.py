from django.urls import path
# obtain_jwt_token是一个视图，其中完成了验证用户名密码签发token的业务
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views.home_views import *
from meiduo_admin.views.user_views import *

urlpatterns = [
    # 登陆接口，签发token
    path('authorizations/', obtain_jwt_token),
    # 用户总数统计
    path('statistical/total_count/', UserTotalCountView.as_view()),
    # 当日新增用户统计
    path('statistical/day_increment/', UserDayCountView.as_view()),
    # 日活跃用户统计
    path('statistical/day_active/', UserActiveCountView.as_view()),
    # 日下单用户统计
    path('statistical/day_orders/', UserOrderCountView.as_view()),
    # 月增用户统计
    path('statistical/month_increment/', UserMonthCountView.as_view()),
    # 获取用户列表数据
    path('users/', UserView.as_view()),
]
