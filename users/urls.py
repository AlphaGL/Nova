from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/update/', views.update_user, name='update_user' )
]
