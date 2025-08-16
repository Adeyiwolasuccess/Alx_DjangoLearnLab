# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post  # <- import Post from your models

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
