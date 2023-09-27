from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["post_text"]

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatars
        fields = ["avatar"]

class BioForm(forms.ModelForm):
    class Meta:
        model = Bio
        fields = ["bio"]

