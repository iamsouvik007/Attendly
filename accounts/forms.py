# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher, TeacherProfile


class TeacherRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Teacher
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class TeacherProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,
        label='Name',
        error_messages={'required': 'Name is required.'},
    )
    mobile_no = forms.CharField(
        required=True,
        label='Mobile No',
        error_messages={'required': 'Mobile No is required.'},
    )

    class Meta:
        model = TeacherProfile
        fields = ['full_name', 'mobile_no']

    def clean_mobile_no(self):
        mobile_no = (self.cleaned_data.get('mobile_no') or '').strip()
        if len(mobile_no) < 10:
            raise forms.ValidationError(
                'Mobile No must be at least 10 digits.')
        if not mobile_no.isdigit():
            raise forms.ValidationError('Mobile No must contain digits only.')
        return mobile_no
