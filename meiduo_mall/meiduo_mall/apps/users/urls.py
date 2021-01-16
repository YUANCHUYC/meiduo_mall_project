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
    # 用户登陆 —— 传统登陆
    path('login/', views.LoginView.as_view()),
    # 用户中心
    path('info/', views.UserInfoView.as_view()),
    # 退出登陆
    path('logout/', views.LogoutView.as_view()),
    # 邮箱
    path('emails/', views.EmailView.as_view()),
    # 激活邮箱
    path('emails/verification/', views.VerifyEmailView.as_view()),
    # 修改密码
    path('password/', views.ChangePasswordView.as_view()),
    # 新增用户地址
    path('addresses/create/', views.CreateAddressView.as_view()),
    # 展示用户地址
    path('addresses/', views.AddressView.as_view()),
    # 更新和删除地址
    path('addresses/<int:address_id>/', views.UpdateDestroyAddressView.as_view()),
    # 设置默认地址
    path('addresses/<int:address_id>/default/', views.DefaultAddressView.as_view()),
    # 设置地址标题
    path('addresses/<int:address_id>/title/', views.UpdateTitleAddressView.as_view()),
    # 记录浏览历史
    path('browse_histories/', views.UserBrowseHistory.as_view()),
]
