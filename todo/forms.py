# todo/forms.py
from django import forms
from .models import Task, Note, Habit, HabitLog

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
        required=False
    )
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'due_date', 'priority', 'recurrence', 'completed'
        ]
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
            'priority': forms.Select(attrs={'class': 'input-field'}),
            'recurrence': forms.Select(attrs={'class': 'input-field'}),
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox-field'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Note title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'input-field',
                'placeholder': 'Write your note here...',
                'rows': 4,
            }),
        }

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'frequency']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Habit name (e.g., Read 30 min)',
            }),
            'frequency': forms.Select(attrs={'class': 'input-field'}),
        }

class HabitLogForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'input-field'})
    )
    class Meta:
        model = HabitLog
        fields = ['date', 'completed']
        widgets = {
            'completed': forms.CheckboxInput(attrs={'class': 'checkbox-field'}),
        }
