import uuid
from uuid import uuid4
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('You must have an Email Address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            email,
            password=password
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=100,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


def profile_pic_filename(instance, filename):
    ext = filename.split('.')[1]
    new_filename = f'{uuid4()}.{ext}'
    return f'profile_pics/{new_filename}'


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    following = models.ManyToManyField(CustomUser, related_name='following', blank=True)


    profile_picture = models.ImageField(upload_to=profile_pic_filename, default='profile_pics/default_profile.png')
    website = models.URLField(blank=True, max_length=200)
    country = CountryField(default='TZ', verbose_name='Country')
    location = models.CharField(max_length=200)
    display_email = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    #Social media links
    youtube_link = models.URLField(verbose_name='Youtube URL')
    facebook_link = models.URLField(verbose_name='Facebook URL')
    instagram_link = models.URLField(verbose_name='Instagram URL')
    linkedin_link = models.URLField(verbose_name='Linkedin URL')

    def __str__(self):
        return self.user.email

    def profiles_posts(self):
        return self.post_set.all()

    def get_absolute_url(self):
        return reverse('main:homepage')

    class Meta:
        ordering = ('-created_at',)