from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Video(models.Model):
    youtube_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    channel_title = models.CharField(max_length=100, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.URLField(blank=True)
    duration = models.DurationField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    # Relationships
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_videos', blank=True)
    
    def __str__(self):
        return self.title

class Collection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')
    videos = models.ManyToManyField(Video, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} (by {self.owner.username})"

class Suggestion(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=RATING_CHOICES)
    
    class Meta:
        unique_together = ('user', 'video')
    def __str__(self):
        return f"{self.score} stars for {self.video} by {self.user}"
