from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='vault'),
    path('nova/', views.home, name='vault_home'),
    path('search/', views.home, name='search'),  # same as home, handles query param
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('category/<slug:slug>/', views.category_videos, name='category_videos'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('favorites/', views.favorites, name='favorites'),
    path('collections/', views.collections, name='collections'),
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('login/', auth_views.LoginView.as_view(template_name='videos/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
