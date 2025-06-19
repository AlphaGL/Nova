# todo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import date, timedelta, datetime
import json
import calendar as calmod

from .models import Task, Note, PomodoroSession, Habit, HabitLog
from .forms import TaskForm, NoteForm, HabitForm, HabitLogForm

# --- Dashboard ---
@login_required
def dashboard(request):
    today = date.today()
    # Today's incomplete tasks
    todays_tasks = Task.objects.filter(user=request.user, due_date=today, completed=False)
    # Upcoming tasks next 7 days
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        due_date__gt=today,
        due_date__lte=today + timedelta(days=7),
        completed=False
    ).order_by('due_date')
    # Stats: completed in last 7 days
    week_ago = today - timedelta(days=7)
    weekly_completed = Task.objects.filter(
        user=request.user,
        completed=True,
        completed_at__date__gte=week_ago
    ).count()
    # Habits overview: list habits and whether logged today
    habits = Habit.objects.filter(user=request.user)
    habit_status = []
    for habit in habits:
        exists = HabitLog.objects.filter(
            habit=habit, date=today
        ).first()
        habit_status.append((habit, exists.completed if exists else False))
    context = {
        'todays_tasks': todays_tasks,
        'upcoming_tasks': upcoming_tasks,
        'weekly_completed': weekly_completed,
        'habit_status': habit_status,
    }
    return render(request, 'todo/dashboard.html', context)


# --- Task CRUD ---
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date', '-priority')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            # If marking completed now, set completed_at
            if task.completed and not task.completed_at:
                task.completed_at = timezone.now()
            task.save()
            return redirect('todo:task_list')
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            t = form.save(commit=False)
            # If newly completed, set completed_at
            if t.completed and not t.completed_at:
                t.completed_at = timezone.now()
            # If un-checking completed, clear completed_at
            if not t.completed:
                t.completed_at = None
            t.save()
            return redirect('todo:task_list')
    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('todo:task_list')
    # optional: confirm page; here we delete directly
    task.delete()
    return redirect('todo:task_list')

@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    if task.completed:
        task.completed_at = timezone.now()
    else:
        task.completed_at = None
    task.save()
    return redirect('todo:task_list')

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    notes = task.notes.all().order_by('-created_at')
    return render(request, 'todo/task_detail.html', {'task': task, 'notes': notes})


# --- Note Create ---
class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'todo/note_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Ensure task exists and belongs to user
        self.task = get_object_or_404(Task, pk=kwargs['task_id'], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task = self.task
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task  # ✅ Add task to context so template can use it
        return context

    def get_success_url(self):
        return reverse_lazy('todo:task_detail', kwargs={'pk': self.task.pk})

# --- Calendar Views ---
@login_required
def calendar_view(request):
    # Renders a template with FullCalendar or custom calendar
    return render(request, 'todo/calendar.html')

@login_required
def calendar_data(request):
    # Return JSON for FullCalendar
    tasks = Task.objects.filter(user=request.user, due_date__isnull=False)
    events = []
    for task in tasks:
        color = {0: 'gray', 1: 'blue', 2: 'red'}.get(task.priority, 'blue')
        events.append({
            'id': task.id,
            'title': task.title,
            'start': task.due_date.isoformat(),
            'color': color,
            'allDay': True,
            'completed': task.completed,
        })
    return JsonResponse(events, safe=False)

@login_required
@csrf_exempt
def update_task_date(request):
    # Handle AJAX drag/drop from FullCalendar
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('id')
            new_date = data.get('start')  # ISO date string
            if task_id and new_date:
                task = Task.objects.get(pk=task_id, user=request.user)
                dt = datetime.fromisoformat(new_date)
                task.due_date = dt.date()
                task.save()
                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponseBadRequest()

# --- Pomodoro Timer ---
@login_required
def pomodoro_timer(request):
    # Show timer page and recent sessions
    sessions = PomodoroSession.objects.filter(user=request.user).order_by('-start_time')[:10]
    tasks = Task.objects.filter(user=request.user, completed=False)
    return render(request, 'todo/pomodoro.html', {'sessions': sessions, 'tasks': tasks})

@login_required
@csrf_exempt
def pomodoro_end(request):
    # AJAX endpoint to record end of a Pomodoro session
    if request.method == 'POST':
        data = json.loads(request.body)
        start_str = data.get('start_time')  # ISO format
        # optional: task_id
        task_id = data.get('task_id')
        try:
            start_dt = datetime.fromisoformat(start_str)
            session = PomodoroSession(user=request.user)
            if task_id:
                session.task_id = task_id
            session.start_time = start_dt
            session.end_time = timezone.now()
            session.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponseBadRequest()


# --- Habits ---
@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    log_form = HabitLogForm()
    if request.method == 'POST':
        # Logging a habit
        habit_id = request.POST.get('habit_id')
        date_str = request.POST.get('date')
        completed = request.POST.get('completed') == 'on'
        if habit_id and date_str:
            habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
            log_date = datetime.fromisoformat(date_str).date()
            log, created = HabitLog.objects.get_or_create(habit=habit, date=log_date)
            log.completed = completed
            log.save()
        return redirect('todo:habit_list')
    return render(request, 'todo/habit_list.html', {'habits': habits, 'log_form': log_form})

@login_required
def habit_create(request):
    form = HabitForm()
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('todo:habit_list')
    return render(request, 'todo/habit_form.html', {'form': form})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
    return redirect('todo:habit_list')
