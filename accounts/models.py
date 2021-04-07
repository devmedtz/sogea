import uuid
from uuid import uuid4
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import models
from django_countries.fields import CountryField



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Staff must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, password=None, *args, **kwargs):

        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_active = True
        is_admin=True
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
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_superuser


def profile_pic_filename(instance, filename):
    ext = filename.split('.')[1]
    new_filename = f'{uuid4()}.{ext}'
    return f'profile_pics/{new_filename}'


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    following = models.ManyToManyField(CustomUser, related_name='follows', blank=True, symmetrical=False)

 
    profile_picture = models.ImageField(upload_to=profile_pic_filename, default='profile_pics/default_profile.png')
    website = models.URLField(blank=True, max_length=200)
    country = CountryField(default='TZ', verbose_name='Country')
    location = models.CharField(max_length=200)
    display_email = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    #Social media links
    youtube_link = models.URLField(verbose_name='Youtube URL', blank=True, null=True)
    facebook_link = models.URLField(verbose_name='Facebook URL', blank=True, null=True)
    instagram_link = models.URLField(verbose_name='Instagram URL', blank=True, null=True)
    linkedin_link = models.URLField(verbose_name='Linkedin URL', blank=True, null=True)
    twitter_link = models.URLField(verbose_name='Twitter URL', blank=True, null=True)
    github_link = models.URLField(verbose_name='Github URL', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
       unique_together = (("user", "following"),)

    @property
    def profiles_posts(self):
        return self.post_set.all()

    @property
    def total_follower(self):
        return self.following.count()  

    def get_absolute_url(self):
        return reverse('account:profile_detail', kwargs={'username':self.user.username})

    class Meta:
        ordering = ('-created_at',)