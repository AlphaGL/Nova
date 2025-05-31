from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'vault'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='vault'),
    path('nova/', views.search_view, name='search'),                # Search page (home)
    path('video/<str:yt_id>/', views.video_detail, name='video_detail'),
    path('favorite/<int:video_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('collections/', views.collections_list, name='collections_list'),
    path('collections/create/', views.create_collection, name='create_collection'),
    path('collections/<int:collection_id>/', views.add_to_collection, name='add_to_collection'),
    path('suggest/', views.suggestion_view, name='suggestion'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('rate/', views.add_rating, name='add_rating'),
]
