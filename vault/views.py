from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Video, Category, Favorite, Collection, Suggestion
from .forms import SuggestionForm, CollectionForm, SignUpForm
from django.http import JsonResponse
from django.conf import settings
import requests


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'vault/index.html'


def home(request):
    """
    Home/search view: lists videos (filtered by search query if given) and shows categories.
    """
    query = request.GET.get('q')
    if query:
        videos = Video.objects.filter(title__icontains=query)
    else:
        videos = Video.objects.all()
    categories = Category.objects.all()
    return render(request, 'videos/home.html', {
        'videos': videos, 'categories': categories
    })

def video_detail(request, video_id):
    """
    Video detail page: displays embedded YouTube player and metadata (views, duration, uploader).
    Metadata is fetched via the YouTube Data API.
    """
    video = get_object_or_404(Video, id=video_id)
    youtube_api_key = settings.YOUTUBE_API_KEY  # (Define this in settings or env)
    api_url = (
        f"https://www.googleapis.com/youtube/v3/videos"
        f"?part=statistics,contentDetails,snippet"
        f"&id={video.youtube_id}&key={youtube_api_key}"
    )
    resp = requests.get(api_url)
    data = resp.json().get('items', [])
    metadata = {}
    if data:
        item = data[0]
        metadata = {
            'views': item['statistics'].get('viewCount'),
            'duration': item['contentDetails'].get('duration'),
            'uploader': item['snippet'].get('channelTitle'),
        }
    # Check if user has favorited this video
    is_fav = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, video=video).exists()
    return render(request, 'videos/video_detail.html', {
        'video': video, 'metadata': metadata, 'is_favorite': is_fav
    })

def category_videos(request, slug):
    """
    Lists videos belonging to a given category.
    """
    category = get_object_or_404(Category, slug=slug)
    videos = category.videos.all()
    return render(request, 'videos/categories.html', {
        'category': category, 'videos': videos
    })

@login_required
def favorites(request):
    """
    Displays the logged-in user’s favorite videos.
    """
    favs = Favorite.objects.filter(user=request.user).select_related('video')
    return render(request, 'videos/favorites.html', {'favorites': favs})

@login_required
def toggle_favorite(request):
    """
    AJAX endpoint to add/remove a favorite. Expects POST with 'video_id'.
    Returns JSON with action status.
    """
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        video = get_object_or_404(Video, id=video_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, video=video)
        if not created:
            fav.delete()
            action = 'removed'
        else:
            action = 'added'
        return JsonResponse({'status': 'ok', 'action': action})
    return JsonResponse({'status': 'invalid'}, status=400)

@login_required
def collections(request):
    """
    Create new collection and list existing collections for the user.
    """
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            coll = form.save(commit=False)
            coll.user = request.user
            coll.save()
            form.save_m2m()
            return redirect('collections')
    else:
        form = CollectionForm()
    user_collections = Collection.objects.filter(user=request.user)
    return render(request, 'videos/collections.html', {
        'collections': user_collections, 'form': form
    })

def suggestions(request):
    """
    Resource suggestion form. Anyone can submit.
    """
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            if request.user.is_authenticated:
                suggestion.user = request.user
            suggestion.save()
            return redirect('home')
    else:
        form = SuggestionForm()
    return render(request, 'videos/suggestions.html', {'form': form})