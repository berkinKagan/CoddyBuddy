from django.urls import path
from . import views

urlpatterns = [
    path('', views.getPost),
    path('posts/', views.getObjects),
    path('posts/<str:pk>', views.getObject),
]
