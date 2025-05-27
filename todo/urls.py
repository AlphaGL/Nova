from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('toggle/<int:pk>/', views.toggle_complete, name='toggle_complete'),
]
