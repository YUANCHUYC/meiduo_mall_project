from django.urls import re_path, path
from . import views

urlpatterns = [
    # 支付接口2：保存支付订单
    path('payment/status/', views.PaymentStatusView.as_view()),

    # 支付接口1：获取支付链接
    path('payment/<str:order_id>/', views.PaymentView.as_view()),
]
