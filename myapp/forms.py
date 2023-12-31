from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        model=User 
        fields=["username", "first_name", "last_name", "email"]

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields="__all__"