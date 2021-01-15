from django.urls import re_path, path
from . import views

# 路由映射列表
urlpatterns = [
    # 路由映射公式： 请求方式 + 路径 = 视图函数
    # GET + usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count = UsernameCountView.get()
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 手机号重复
    path('mobiles/<mobile:mobile>/count/', views.MobileCountView.as_view()),
    # 用户注册接口
    path('register/', views.RegisterView.as_view()),
]
