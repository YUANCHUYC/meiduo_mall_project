from django.urls import path
from . import views

urlpatterns = [
    # 获取图形验证码
    path('image_codes/<uuid:uuid>/', views.ImageCodeView.as_view()),
    # 发送短信
    path('sms_codes/<mobile:mobile>/', views.SMSCodeView.as_view()),
]
