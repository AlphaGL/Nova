from django.contrib import admin
from .models import Video, Category, Tag, Collection, Suggestion, Rating

admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Collection)
admin.site.register(Suggestion)
admin.site.register(Rating)