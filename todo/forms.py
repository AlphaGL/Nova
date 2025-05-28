from django import forms
from .models import Task

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter task title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Describe your task (optional)',
                'rows': 3,
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'input-field',
                'type': 'date',
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'checkbox-field',
            }),
        }

