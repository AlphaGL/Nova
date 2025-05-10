from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='study_group_home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete_room'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete_message'),

    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    path('topics/', views.topics_page, name='topics')
]