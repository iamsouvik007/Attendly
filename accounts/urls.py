# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.TeacherLoginView.as_view(), name='login'),
    path('google/start/', views.GoogleStartView.as_view(), name='google_start'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
