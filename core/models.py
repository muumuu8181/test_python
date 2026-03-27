from django.db import models
from django_summernote.fields import SummernoteTextField

class Page(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = SummernoteTextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
