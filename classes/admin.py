# classes/admin.py

from django.contrib import admin
from .models import Class, Student, Enrollment


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'year', 'teacher']
    search_fields = ['name', 'code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'student_id', 'phone']
    search_fields = ['student_id', 'first_name', 'last_name']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_enrolled', 'enrolled_at']
