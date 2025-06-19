# todo/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Task(models.Model):
    user = models.ForeignKey(
        'users.User',  # or settings.AUTH_USER_MODEL
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    PRIORITY_CHOICES = [
        (0, 'Low'),
        (1, 'Medium'),
        (2, 'High'),
    ]
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)

    RECURRENCE_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    recurrence = models.CharField(
        max_length=10,
        choices=RECURRENCE_CHOICES,
        default='none'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Detect change to completed from False->True to schedule next occurrence
        is_new = self.pk is None
        old_completed = None
        if not is_new:
            prev = Task.objects.filter(pk=self.pk).first()
            if prev:
                old_completed = prev.completed
        super().save(*args, **kwargs)

        # If it just got completed, and has recurrence, create next occurrence
        if self.recurrence != 'none' and self.completed:
            if old_completed is False or is_new:
                # Only schedule if previously not completed
                if self.due_date:
                    if self.recurrence == 'daily':
                        next_due = self.due_date + timedelta(days=1)
                    elif self.recurrence == 'weekly':
                        next_due = self.due_date + timedelta(weeks=1)
                    elif self.recurrence == 'monthly':
                        # Approximate: add 1 month by adding 30 days
                        next_due = self.due_date + timedelta(days=30)
                    else:
                        next_due = None

                    if next_due:
                        Task.objects.create(
                            user=self.user,
                            title=self.title,
                            description=self.description,
                            due_date=next_due,
                            priority=self.priority,
                            recurrence=self.recurrence
                        )

class Note(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='notes'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.task.title}: {self.title}"

class PomodoroSession(models.Model):
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pomodoro by {self.user} at {self.start_time}"

    @property
    def duration_minutes(self):
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.seconds // 60
        return None

class Habit(models.Model):
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, default='daily'
    )

    def __str__(self):
        return f"{self.name} ({self.frequency})"

class HabitLog(models.Model):
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name='logs'
    )
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f"{self.habit.name} on {self.date}: {'Done' if self.completed else 'Not done'}"
