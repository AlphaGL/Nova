from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatThread, ChatMessage
from .ai_engine import generateChatResponse

@login_required
def chat_home(request):
    threads = ChatThread.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'smart_tutor/index.html', {'threads': threads})

@login_required
def chat_thread(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)

    if request.method == 'POST':
        user_msg = request.POST.get('prompt')
        user_chat = ChatMessage.objects.create(thread=thread, sender='user', content=user_msg)
        ai_response = generateChatResponse(user_msg)
        ai_chat = ChatMessage.objects.create(thread=thread, sender='ai', content=ai_response)
        return JsonResponse({'answer': ai_response})

    messages = thread.messages.order_by('timestamp')
    return render(request, 'smart_tutor/chat_thread.html', {'thread': thread, 'messages': messages})

@login_required
def create_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        thread = ChatThread.objects.create(user=request.user, title=title)
        return redirect('chat_thread', thread_id=thread.id)
    return render(request, 'smart_tutor/create_thread.html')

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, thread__user=request.user)
    thread_id = message.thread.id
    message.delete()
    return redirect('chat_thread', thread_id=thread_id)

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, thread__user=request.user)
    if request.method == 'POST':
        message.content = request.POST.get('content')
        message.save()
        return redirect('chat_thread', thread_id=message.thread.id)
    return render(request, 'smart_tutor/edit_message.html', {'message': message})
