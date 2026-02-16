from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = SummernoteTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=100, default='General')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
