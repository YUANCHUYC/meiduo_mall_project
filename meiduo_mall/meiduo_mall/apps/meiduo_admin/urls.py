from django.urls import path
# obtain_jwt_token是一个视图，其中完成了验证用户名密码签发token的业务
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views.home_views import *
from meiduo_admin.views.user_views import *
from meiduo_admin.views.sku_views import *

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

    # SKU列表数据和单一新建
    path('skus/', SKUGoodsView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    # SKU单一数据，更新和删除
    path('skus/<int:pk>/', SKUGoodsView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新建SKU可选三级分类列表数据
    path('skus/categories/', SKUGoodsCateView.as_view()),
    # 新建SKU可选SPU列表数据
    path('goods/simple/', SPUSimpleView.as_view()),
    # 新建SKU用户选择的SPU所关联的规格和选项信息
    path('goods/<int:pk>/specs/', SpecOptView.as_view()),
]
