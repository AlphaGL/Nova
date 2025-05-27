from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

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
