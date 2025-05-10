from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/messages/user_<id>/<filename>
    return f'messages/user_{instance.user.id}/{filename}'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    media = models.FileField(upload_to='messages/', null=True, blank=True)
    update = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] if self.body else "Media Message"