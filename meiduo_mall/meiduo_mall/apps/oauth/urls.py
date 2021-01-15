from django.urls import path, re_path
from . import views

# 路由映射列表
urlpatterns = [
    # qq登陆接口1
    path('qq/authorization/', views.QQURLView.as_view()),
    # qq登陆接口2和接口3
    path('oauth_callback/', views.QQUserView.as_view()),
]
