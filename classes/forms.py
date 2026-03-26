from django import forms
from .models import Class, Student


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'code', 'year']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'phone']
        labels = {
            'student_id': 'Roll No',
            'phone': 'Phone No',
        }
