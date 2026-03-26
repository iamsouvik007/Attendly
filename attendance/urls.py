from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('start/<int:class_pk>/', views.StartSessionView.as_view(), name='start'),
    path('mark/<int:session_pk>/', views.MarkAttendanceView.as_view(), name='mark'),
]