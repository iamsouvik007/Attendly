from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('class/<int:class_pk>/', views.ClassReportView.as_view(), name='class_report'),
    path('student/<int:student_pk>/', views.StudentReportView.as_view(), name='student_report'),
]