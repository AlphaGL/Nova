# todo/urls.py
from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Task CRUD
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:pk>/toggle/', views.toggle_complete, name='toggle_complete'),

    # Notes
    path('tasks/<int:task_id>/notes/add/', views.NoteCreateView.as_view(), name='note_add'),

    # Calendar
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/data/', views.calendar_data, name='calendar_data'),
    path('calendar/update-date/', views.update_task_date, name='update_task_date'),

    # Pomodoro
    path('pomodoro/', views.pomodoro_timer, name='pomodoro_timer'),
    path('pomodoro/end/', views.pomodoro_end, name='pomodoro_end'),

    # Habits
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/add/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
]
