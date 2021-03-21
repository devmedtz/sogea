import uuid
import readtime
from uuid import uuid4
from django.utils import timezone
from datetime import datetime
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image

from comment.models import Comment
from .choices import *
from accounts.models import Profile

User = get_user_model()

def featured_image_path(instance, filename):
    return f"{instance.author.pk}/posts/{instance.title}/{filename}/"

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    title = models.CharField(max_length=250)
    slug = models.SlugField(default='', max_length=250, editable=False, unique=True)
    content = RichTextUploadingField(blank=False)
    view_count = models.PositiveIntegerField(default=0)
    comments = GenericRelation(Comment)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to=featured_image_path)
    featured = models.BooleanField(default=False)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    status = models.CharField(max_length=100, choices=STATUS, default='Pending')
    
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        kwargs = {
            'post_slug': self.slug
        }
        return reverse('main:post_detail', kwargs=kwargs)

    @property
    def total_likes(self):
        return self.likes.count()

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        if not self.slug:
            random_code = datetime.now().strftime('%H%M%S')
            self.slug = str(random_code) + "-" + slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "comment"


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "reply"


class PostBookmark(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post.title)

    @property
    def total_bookmark(self):
        return self.post.count()

