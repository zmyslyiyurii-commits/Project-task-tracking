from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('create/', views.create_item, name='create_item'),
    path('logout/', views.logout_view, name='logout'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
]