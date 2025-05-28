from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils.dateformat import DateFormat
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
from django.db.models.functions import TruncDate
from django.db.models import Count
import calendar
from datetime import date, datetime

@login_required
def custom_calendar_view(request):
    # Get current year and month from query params or default to today
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))

    # Get tasks for this user filtered by year/month
    tasks = Task.objects.filter(user=request.user, due_date__year=year, due_date__month=month)

    # Group tasks by due_date
    tasks_by_date = {}
    for task in tasks:
        key = task.due_date.strftime("%Y-%m-%d")
        if key not in tasks_by_date:
            tasks_by_date[key] = {'tasks': [], 'all_completed': True}
        tasks_by_date[key]['tasks'].append({'title': task.title, 'completed': task.completed})
        if not task.completed:
            tasks_by_date[key]['all_completed'] = False



    # Get calendar matrix for the month (weeks and days)
    cal = calendar.Calendar(firstweekday=6)  # week starts on Sunday (6)
    month_days = cal.monthdatescalendar(year, month)  # list of weeks with date objects

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_days': month_days,
        'tasks_by_date': tasks_by_date,
    }
    return render(request, 'todo/custom_calendar.html', context)


@csrf_exempt
def update_task_date(request, task_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_date = parse_date(data['new_date'])
            task = Task.objects.get(id=task_id)
            task.due_date = new_date
            task.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def calendar_view(request):
    return render(request, 'todo/calendar.html')

@login_required
def calendar_data(request):
    tasks = Task.objects.filter(user=request.user)
    events = []

    for task in tasks:
        events.append({
            "id": task.id,  # important for update and identification
            "title": task.title,
            "start": task.due_date.isoformat(),
            "color": "#4caf50" if task.completed else "#f44336"
        })
    return JsonResponse(events, safe=False)


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')

    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})


@login_required
def edit_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'todo/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def toggle_complete(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
