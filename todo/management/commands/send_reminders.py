# todo/management/commands/send_reminders.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from todo.models import Task

class Command(BaseCommand):
    help = "Send email reminders for tasks due within the next day"

    def handle(self, *args, **options):
        today = timezone.now().date()
        # Tasks due tomorrow (or within next 24h). Adjust as needed.
        upcoming = Task.objects.filter(
            due_date__isnull=False,
            due_date__lte=today + timedelta(days=1),
            due_date__gte=today,
            completed=False
        )
        for task in upcoming:
            user = task.user
            if not user.email:
                continue
            subject = f"Reminder: Task '{task.title}' due {task.due_date}"
            message = (
                f"Hello {user.get_full_name() or user.username},\n\n"
                f"This is a reminder that your task \"{task.title}\" is due on {task.due_date}.\n"
                "Please make sure to complete it on time.\n\n"
                "Regards,\nPlanner App"
            )
            send_mail(
                subject,
                message,
                None,  # uses DEFAULT_FROM_EMAIL
                [user.email],
                fail_silently=False,
            )
            self.stdout.write(f"Sent reminder for task {task.id} to {user.email}")
