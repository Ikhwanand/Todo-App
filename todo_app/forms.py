from django import forms 
from .models import Task 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task 
        fields = ['title', 'description', 'completed']
        

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)