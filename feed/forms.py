from django import forms
from .models import Post, Profile, Relationship, Comment  # ← add Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']
        labels = {
            'description': 'What would you like to say?',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'dob', 'bio']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'dob': 'Date of Birth',
            'bio': 'Bio',
        }

class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = '__all__'
        labels = {
            'sender': 'Accept friend request from:',
            'receiver': 'Send friend request to:',
            'status': 'Current status:',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']                   # matches your Comment model
        labels = {'text': 'Add a comment'}

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
