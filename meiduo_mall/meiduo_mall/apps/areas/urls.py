from django.urls import path, re_path
from . import views

urlpatterns = [
    # 获取省份信息
    path('areas/', views.ProvinceAreasView.as_view()),
    # 获取子级行政区信息
    path('areas/<int:pk>/', views.SubAreasView.as_view()),
]
