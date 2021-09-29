from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.db.models import Q
# from tinymce import HTMLField
from django.template.defaultfilters import slugify



class PostView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='4. PostView'

    def __str__(self):
        return self.user.email

class Author(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField()
    detail = models.TextField(max_length=100)

    class Meta:
        verbose_name_plural='1. Author'

    def __str__(self):
        return self.user.email


class Blog_Category(models.Model):
    title = models.CharField(max_length=20)
    detail = models.TextField(blank=True)
    featured = models.BooleanField(default=True)
 
    # post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "2. Categories"
    
    def __str__(self):
        return self.title
    # def get_absolute_url(self):
    #     return reverse('post-category', args=[self.title])
    def get_absolute_url(self):
        return reverse('post-category', kwargs={
            'slug': self.slug
        })

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    featured = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #content = HTMLField()
    user = models.ForeignKey(Author,on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    category = models.ForeignKey(Blog_Category, related_name='categories', on_delete=models.CASCADE)
    tags = TaggableManager()
    slug = models.SlugField(null=False, unique=True)


    class Meta:
        verbose_name_plural='3. Post'


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'slug': self.slug
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'slug': self.slug
        })