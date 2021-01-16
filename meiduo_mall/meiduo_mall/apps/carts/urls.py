from django.urls import re_path, path
from . import views

urlpatterns = [
    path('carts/', views.CartsView.as_view()),
    path('carts/selection/', views.CartsSelectAllView.as_view()),
    path('carts/simple/', views.CartsSimpleView.as_view()),
]
