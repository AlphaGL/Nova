# todo/admin.py
from django.contrib import admin
from .models import Task, Note, PomodoroSession, Habit, HabitLog

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'recurrence', 'completed')
    list_filter = ('priority', 'recurrence', 'completed')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'created_at')

@admin.register(PomodoroSession)
class PomodoroAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'start_time', 'end_time')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'frequency')

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed')
    list_filter = ('completed',)
