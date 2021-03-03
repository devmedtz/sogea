import uuid
from uuid import uuid4
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from .choices import *
from accounts.models import CustomUser

User = get_user_model()

def profile_pic_filename(instance, filename):
    ext = filename.split('.')[1]
    new_filename = f'{uuid4()}.{ext}'
    return f'profile_pics/{new_filename}'

def featured_image(instance, filename):
    ext = filename.split('.')[1]
    new_filename = f'{uuid4()}.{ext}'
    return f'featured_pics/{new_filename}'

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=250)
    slug = models.SlugField(default='', max_length=250, editable=False)

    content = RichTextUploadingField(blank=False)

    comment_count = models.IntegerField(default = 0)
    view_count = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    featured_image = models.ImageField(upload_to=featured_image)

    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='uncategorized')

    featured = models.BooleanField(default=False)

    language = models.CharField(max_length=20, choices=LANGUAGE)

    tags = TaggableManager()

    # likes = models,

    status = models.CharField(max_length=100, choices=STATUS, default='Pending')

    membership = models.CharField(max_length=100, choices=MEMBERSHIP)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4()) + "/" + slugify(self.title)
        return super().save(*args, **kwargs)

