from django.urls import path, re_path
from . import views

urlpatterns = [
    # 结算接口
    path('orders/settlement/', views.OrderSettlementView.as_view()),
    # 下订单
    path('orders/commit/', views.OrderCommitView.as_view()),
]
