# sync_data.py

import os
import django
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")  # Change to your actual project name
django.setup()

from users.models import User
from study_tracker.models import Semester, Grade, Course
from todo.models import Task, Note, PomodoroSession, Habit, HabitLog

def sync_users(db1, db2):
    print("👥 Syncing Users...")
    for user in User.objects.using(db1).all():
        User.objects.using(db2).update_or_create(
            id=user.id,
            defaults={
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'bio': user.bio,
                'avatar': user.avatar,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'password': user.password,  # preserves password hash
            }
        )
        print(f"✅ Synced user: {user.email}")
    print("✅ Finished syncing users.\n")

def sync_cgpa_app(db1, db2):
    print("📘 Syncing CGPA App...")

    for grade in Grade.objects.using(db1).all():
        Grade.objects.using(db2).update_or_create(
            id=grade.id,
            defaults={
                'letter': grade.letter,
                'points': grade.points
            }
        )

    for semester in Semester.objects.using(db1).all():
        user = User.objects.using(db2).get(id=semester.user.id)
        Semester.objects.using(db2).update_or_create(
            id=semester.id,
            defaults={
                'user': user,
                'name': semester.name,
                'year': semester.year
            }
        )

    for course in Course.objects.using(db1).all():
        user = User.objects.using(db2).get(id=course.user.id)
        semester = Semester.objects.using(db2).get(id=course.semester.id)
        grade = Grade.objects.using(db2).get(id=course.grade.id)

        Course.objects.using(db2).update_or_create(
            id=course.id,
            defaults={
                'user': user,
                'semester': semester,
                'name': course.name,
                'credits': course.credits,
                'grade': grade
            }
        )

    print("✅ CGPA App Synced.\n")

def sync_todo_app(db1, db2):
    print("📝 Syncing Todo App...")

    for task in Task.objects.using(db1).all():
        user = User.objects.using(db2).get(id=task.user.id)
        Task.objects.using(db2).update_or_create(
            id=task.id,
            defaults={
                'user': user,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'created_at': task.created_at,
                'completed': task.completed,
                'completed_at': task.completed_at,
                'priority': task.priority,
                'recurrence': task.recurrence,
            }
        )

    for note in Note.objects.using(db1).all():
        task = Task.objects.using(db2).get(id=note.task.id)
        Note.objects.using(db2).update_or_create(
            id=note.id,
            defaults={
                'task': task,
                'title': note.title,
                'content': note.content,
                'created_at': note.created_at,
            }
        )

    for session in PomodoroSession.objects.using(db1).all():
        user = User.objects.using(db2).get(id=session.user.id)
        task = Task.objects.using(db2).filter(id=session.task.id).first() if session.task else None
        PomodoroSession.objects.using(db2).update_or_create(
            id=session.id,
            defaults={
                'user': user,
                'task': task,
                'start_time': session.start_time,
                'end_time': session.end_time,
            }
        )

    for habit in Habit.objects.using(db1).all():
        user = User.objects.using(db2).get(id=habit.user.id)
        Habit.objects.using(db2).update_or_create(
            id=habit.id,
            defaults={
                'user': user,
                'name': habit.name,
                'frequency': habit.frequency,
            }
        )

    for log in HabitLog.objects.using(db1).all():
        habit = Habit.objects.using(db2).get(id=log.habit.id)
        HabitLog.objects.using(db2).update_or_create(
            id=log.id,
            defaults={
                'habit': habit,
                'date': log.date,
                'completed': log.completed,
            }
        )

    print("✅ Todo App Synced.\n")

def sync_all():
    db1 = 'default'
    db2 = 'db2'

    sync_users(db1, db2)
    sync_cgpa_app(db1, db2)
    sync_todo_app(db1, db2)
    print("🎉 All data successfully synced from default → db2")

if __name__ == "__main__":
    sync_all()
