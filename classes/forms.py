from django import forms
from .models import Class, Student


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'code', 'year']


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        error_messages={'required': 'First name is required.'},
    )
    last_name = forms.CharField(
        required=True,
        error_messages={'required': 'Last name is required.'},
    )
    student_id = forms.CharField(
        required=True,
        label='Roll No',
        error_messages={'required': 'Roll No is required.'},
    )
    phone = forms.CharField(
        required=True,
        label='Mobile No',
        error_messages={'required': 'Mobile No is required.'},
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'phone']
        labels = {
            'student_id': 'Roll No',
            'phone': 'Mobile No',
        }

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if len(phone) < 10:
            raise forms.ValidationError(
                'Mobile No must be at least 10 digits.')
        if not phone.isdigit():
            raise forms.ValidationError('Mobile No must contain digits only.')
        return phone
