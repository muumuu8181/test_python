from django.shortcuts import render, get_object_or_404
from .models import Page
from news.models import Post

def home(request):
    # Get latest 3 published posts
    latest_posts = Post.objects.filter(status='published').order_by('-created_on')[:3]
    return render(request, 'core/home.html', {'latest_posts': latest_posts})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, status='published')
    return render(request, 'core/page_detail.html', {'page': page})
