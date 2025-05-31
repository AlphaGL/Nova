# vault/models.py

from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=20, unique=True)
    channel = models.CharField(max_length=200, blank=True)  # optional channel name
    categories = models.ManyToManyField(Category, related_name='videos', blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)
    videos = models.ManyToManyField(Video, related_name='in_collections', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    video_url = models.URLField(help_text="URL of suggested video/resource")
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
