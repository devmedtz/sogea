import uuid
import os
from uuid import uuid4
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=250)
    slug = models.SlugField(default='', max_length=250, editable=False, unique=True)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published = models.CharField(max_length=50)
    pages = models.PositiveIntegerField(default=1)
    downloads = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='books/thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.FileField(upload_to='books/all-books/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)

        if not self.slug:
            random_code = datetime.now().strftime('%H%M%S')
            self.slug = str(random_code) + "-" + slugify(self.title)
        return super().save(*args, **kwargs)

