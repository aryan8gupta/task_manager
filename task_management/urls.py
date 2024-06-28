from django.urls import path
from task_management import views

urlpatterns = [
    path('', views.home),
    path('signin/', views.signin),
    path('login/', views.login),
    path('dashboard/', views.dashboard),
    path('read/', views.read),
    path('create/', views.create),
    path('update/', views.update),
    path('detail/', views.detail),
    path('delete/', views.delete),
]
