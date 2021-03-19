from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

from .models import Profile

User = get_user_model


@receiver(user_signed_up) 
def populate_profile(user, **kwargs):

    user.profile = Profile()   

    user.profile.user = user
    user.profile.save()

      
