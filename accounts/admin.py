from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from . import forms
from . models import CustomUser, Profile

# Register the new UserAdmin...
admin.site.register(CustomUser)
admin.site.register(Profile)
