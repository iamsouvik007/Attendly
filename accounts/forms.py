# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher


class TeacherRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Teacher
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']