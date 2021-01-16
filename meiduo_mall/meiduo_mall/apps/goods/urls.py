from django.urls import re_path, path
from . import views

urlpatterns = [
    # ......
    # 商品搜索
    path('search/', views.MySearchView()),
    # 商品分页列表数据
    path('list/<int:category_id>/skus/', views.ListView.as_view()),
    # 热销商品
    path('hot/<int:category_id>/', views.HotGoodsView.as_view()),
]
