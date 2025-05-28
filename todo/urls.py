from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('toggle/<int:pk>/', views.toggle_complete, name='toggle_complete'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/data/', views.calendar_data, name='calendar_data'),
    path('custom-calendar/', views.custom_calendar_view, name='custom_calendar_view'),
    path('update-task-date/<int:task_id>/', views.update_task_date, name='update-task-date'),
]
