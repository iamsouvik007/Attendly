# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, TeacherProfile


@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    model = Teacher
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    ordering = ['email']

    # Override because we removed username
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'phone', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'full_name', 'mobile_no', 'updated_at']
    search_fields = ['teacher__email', 'full_name', 'mobile_no']
