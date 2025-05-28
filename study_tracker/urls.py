# cgpa_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='study_tracker_home'),  # e.g., list of semesters
    path('semester/<int:semester_id>/', views.semester_detail, name='semester-detail'),
    path('semester/<int:semester_id>/course/add/', views.add_course, name='course-add'),
    path('course/<int:pk>/edit/', views.edit_course, name='course-edit'),
    path('course/<int:pk>/delete/', views.delete_course, name='course-delete'),
    # ... other routes as needed
]