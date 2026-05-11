from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('create/', views.create_item, name='create_item'),
    path('logout/', views.logout_view, name='logout'),
]