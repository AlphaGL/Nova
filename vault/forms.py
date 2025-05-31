# videos/forms.py

from django import forms
from .models import Suggestion, Collection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'video_url', 'description']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'videos']
        widgets = {
            'videos': forms.CheckboxSelectMultiple,  # multi-select widget
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
