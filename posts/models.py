import uuid
import readtime
from uuid import uuid4
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment
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


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=250)
    slug = models.SlugField(default='', max_length=250, editable=False, unique=True)

    content = RichTextUploadingField(blank=False)

    view_count = models.PositiveIntegerField(default=0)
    # the field name should be comments
    comments = GenericRelation(Comment)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    featured_image = models.ImageField(upload_to=featured_image)

    featured = models.BooleanField(default=False)

    tags = TaggableManager()

    # likes = models,

    status = models.CharField(max_length=100, choices=STATUS, default='Pending')



    def __str__(self):
        return str(self.title)


    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text


    def save(self, *args, **kwargs):
        if not self.slug:
            random_code = datetime.now().strftime('%H%M%S')
            self.slug = str(random_code) + "-" + slugify(self.title)
        return super().save(*args, **kwargs)

