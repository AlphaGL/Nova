from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic,Message
from django.contrib import messages

from users.models import User
from . forms import RoomForm

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        ).order_by('-id')
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-id')[0:5]
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'study_groups/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-id')
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        media = request.FILES.get('media')

        if body or media:  # allow message if either text or media is provided
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                media=media
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        else:
            # Optionally handle the case where both body and media are missing
            pass

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'study_groups/room.html', context)



@login_required(login_url='/users/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('study_group_home')
    context = {'form':form, 'topics':topics}
    return render (request, 'study_groups/room_form.html', context)


@login_required(login_url='/users/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('study_group_home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render (request, 'study_groups/room_form.html', context)

@login_required(login_url='/users/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You can't delete this!!")

    if request.method == 'POST':
        room.delete()
        return redirect('study_group_home')
    return render(request, 'study_groups/delete.html', {'obj':room})


@login_required(login_url='/users/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You can't delete this!!")

    if request.method == 'POST':
        room_id = message.room.id
        message.delete()
        return redirect('room', pk=room_id)

    return render(request, 'study_groups/delete.html', {'obj': message})





def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all().order_by('-id')[0:5]
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'study_groups/profile.html', context)



def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'study_groups/topics.html', {'topics':topics})


def activity_page(request):
    room_messages = Message.objects.all().order_by('-id')[0:5]
    rooms = Room.objects.all()[0:10]
    return render(request, 'study_groups/activity.html', {'room_messages': room_messages, 'rooms':rooms})