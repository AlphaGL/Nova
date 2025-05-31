# videos/forms.py
from django import forms
from .models import Suggestion, Collection


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'url', 'description']

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name']
