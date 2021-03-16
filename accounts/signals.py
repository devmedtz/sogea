from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

from .models import Profile

User = get_user_model

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(user_signed_up) 
def populate_profile(sociallogin, user, **kwargs):

    user.profile = Profile()   

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        picture_url = "not available"
        if len(user_data):
            picture_url = user_data['picture']
        user.profile.profile_picture = picture_url
        user.profile.save()

      
