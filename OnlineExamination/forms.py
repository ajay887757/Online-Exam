from .models import Student
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'password', 'name', 'email', 'phone']
        widgets = {'password': forms.PasswordInput()}



class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
