from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.ClassListView.as_view(), name='list'),
    path('create/', views.ClassCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ClassDetailView.as_view(), name='detail'),
    path('<int:pk>/students/add/',
         views.AddStudentView.as_view(), name='add_student'),
    path('<int:pk>/delete/', views.DeleteClassView.as_view(), name='delete'),
    path('<int:pk>/students/<int:student_pk>/delete/',
         views.DeleteStudentView.as_view(), name='delete_student'),
]
