from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/main.html'

def custom_404_view(request, exception):
    return render(request, 'core/404.html', status=404)