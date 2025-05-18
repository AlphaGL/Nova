from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('thread/<int:thread_id>/', views.chat_thread, name='chat_thread'),
    path('create/', views.create_thread, name='create_thread'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
]
