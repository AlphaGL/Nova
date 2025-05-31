# vaults/views.py
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from googleapiclient.discovery import build
from .models import Video, Collection, Suggestion, Tag, Rating
from .forms import SuggestionForm, CollectionForm
from django.utils.dateparse import parse_duration
from django.db import models


YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY


class HomePageView(TemplateView):
    template_name = 'vault/index.html'

def search_view(request):
    query = request.GET.get('q', '')
    videos = []
    if query:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)  # Google API client
        search_request = youtube.search().list(
            part='id,snippet',
            q=query,
            type='video',
            maxResults=50
        )
        total_fetched = 0
        while search_request and total_fetched < 150:
            response = search_request.execute()
            for item in response.get('items', []):
                total_fetched += 1
                if total_fetched > 150:
                    break
                video_id = item['id']['videoId']
                snippet = item['snippet']
                # Fetch or create Video in DB
                video, created = Video.objects.get_or_create(youtube_id=video_id)
                if created:
                    video.title = snippet['title']
                    video.description = snippet.get('description', '')
                    video.channel_title = snippet.get('channelTitle', '')
                    video.published_at = snippet.get('publishedAt')
                    video.thumbnail_url = snippet['thumbnails']['default']['url']
                    # Fetch additional details (views, duration)
                    detail = youtube.videos().list(part='contentDetails,statistics', id=video_id).execute()
                    if detail['items']:
                        stats = detail['items'][0]['statistics']
                        video.view_count = stats.get('viewCount', 0)
                        duration = detail['items'][0]['contentDetails']['duration']
                        # Convert ISO 8601 duration to Python timedelta (omitted for brevity)
                        video.duration = parse_duration(duration)
                    video.save()
                videos.append(video)
            # Get next page token
            search_request = youtube.search().list(
                part='id,snippet',
                q=query,
                type='video',
                maxResults=50,
                pageToken=response.get('nextPageToken')
            ) if response.get('nextPageToken') else None

        # Paginate results (50 per page)
        paginator = Paginator(videos, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'vault/search_results.html', {'page_obj': page_obj, 'query': query})
    return render(request, 'vault/search_results.html', {})

def video_detail(request, yt_id):
    video = get_object_or_404(Video, youtube_id=yt_id)
    is_favorited = False
    user_rating = None
    if request.user.is_authenticated:
        is_favorited = video in request.user.favorite_videos.all()
        try:
            user_rating = Rating.objects.get(user=request.user, video=video).score
        except Rating.DoesNotExist:
            user_rating = None
    avg_rating = video.ratings.aggregate(models.Avg('score'))['score__avg']
    tags = video.tags.all()
    return render(request, 'vault/vault_detail.html', {
        'video': video,
        'is_favorited': is_favorited,
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'tags': tags,
    })

@login_required
def toggle_favorite(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if video in request.user.favorite_videos.all():
        request.user.favorite_videos.remove(video)
    else:
        request.user.favorite_videos.add(video)
    return redirect('vault:video_detail', yt_id=video.youtube_id)

@login_required
def collections_list(request):
    collections = request.user.collections.all()
    return render(request, 'vault/collections.html', {'collections': collections})

@login_required
def create_collection(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.owner = request.user
            collection.save()
            # Optional email notification to admins
            send_mail(
                subject="New collection created",
                message=f"User {request.user.username} created collection '{collection.name}'",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email for _, email in settings.ADMINS]
            )
            return redirect('vault:collections_list')
    else:
        form = CollectionForm()
    return render(request, 'vault/collection_form.html', {'form': form})

@login_required
def add_to_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, owner=request.user)
    video_id = request.GET.get('video_id')
    video = get_object_or_404(Video, pk=video_id)
    collection.videos.add(video)
    return redirect('vault:video_detail', yt_id=video.youtube_id)

def suggestion_view(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            if request.user.is_authenticated:
                suggestion.user = request.user
            suggestion.save()
            # Email admins about suggestion
            send_mail(
                subject="New suggestion submitted",
                message=f"Title: {suggestion.title}\nURL: {suggestion.url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email for _, email in settings.ADMINS]
            )
            return redirect('vault:search')
    else:
        form = SuggestionForm()
    return render(request, 'vault/suggestion_form.html', {'form': form})

@login_required
def add_tag(request):
    video_id = request.POST.get('video_id')
    tag_name = request.POST.get('tag_name')
    video = get_object_or_404(Video, pk=video_id)
    tag, _ = Tag.objects.get_or_create(name=tag_name)
    video.tags.add(tag)
    return redirect('vault:video_detail', yt_id=video.youtube_id)

@login_required
def add_rating(request):
    video_id = request.POST.get('video_id')
    score = int(request.POST.get('score'))
    video = get_object_or_404(Video, pk=video_id)
    rating, created = Rating.objects.update_or_create(user=request.user, video=video, defaults={'score': score})
    return redirect('vault:video_detail', yt_id=video.youtube_id)