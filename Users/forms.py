from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password']

class LoginForm(forms.Form):
    Login = forms.CharField(max_length=40, widget=forms.TextInput(attrs = {'placeholder': 'Login', 'class': 'Login-input'}))
    Password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'Password-input'}))
    widgets = {
        'Password': forms.PasswordInput(),
        }