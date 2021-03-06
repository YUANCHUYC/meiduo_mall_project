from django.urls import path
# obtain_jwt_token是一个视图，其中完成了验证用户名密码签发token的业务
from rest_framework_jwt.views import obtain_jwt_token

from meiduo_admin.views.home_views import *
from meiduo_admin.views.user_views import *
from meiduo_admin.views.sku_views import *
from meiduo_admin.views.spu_views import *
from meiduo_admin.views.spec_views import *
from meiduo_admin.views.option_views import *
from meiduo_admin.views.image_views import *
from meiduo_admin.views.order_views import *
from meiduo_admin.views.perm_views import *
from meiduo_admin.views.group_views import *
from meiduo_admin.views.admin_views import *

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

    # SPU管理
    path('goods/', SPUModelView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('goods/<int:pk>/', SPUModelView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新建SPU可选品牌
    path('goods/brands/simple/', BrandSimpleView.as_view()),
    # 新建SPU可选一级分类
    path('goods/channel/categories/', CateSimpleListView.as_view()),
    # 新建SPU可选二三级分类
    path('goods/channel/categories/<int:pk>/', CateSimpleListView.as_view()),

    # 规格表管理
    path('goods/specs/', SpecViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('goods/specs/<int:pk>/', SpecViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    # 新建选项可选规格
    path('goods/specs/simple/', SpecSimpleListView.as_view()),
    # 选项表管理
    path('specs/options/', OptionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('specs/options/<int:pk>/', OptionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),

    # 图片管理
    path('skus/images/', ImageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('skus/images/<int:pk>/', ImageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新建图片可选sku
    path('skus/simple/', ImageViewSet.as_view({
        'get': 'simple'
    })),

    # 订单管理
    path('orders/', OrderView.as_view({
        'get': 'list'
    })),
    path('orders/<str:pk>/', OrderView.as_view({
        'get': 'retrieve',
    })),
    path('orders/<str:pk>/status/', OrderView.as_view({
        'patch': 'partial_update'
    })),

    # 权限管理
    path('permission/perms/', PermViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('permission/perms/<int:pk>/', PermViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新增权限可选类型
    path('permission/content_types/', ContentTypeListView.as_view()),

    # 分组管理
    path('permission/groups/', GroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('permission/groups/<int:pk>/', GroupViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新建分组可选权限
    path('permission/simple/', GroupPermListView.as_view()),

    # 管理员管理
    path('permission/admins/', AdminViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('permission/admins/<int:pk>/', AdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    # 新建管理员用户可选分组
    path('permission/groups/simple/', AdminGroupListView.as_view()),
]
