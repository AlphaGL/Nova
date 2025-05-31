from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Favorite)
admin.site.register(Collection)
admin.site.register(Suggestion)