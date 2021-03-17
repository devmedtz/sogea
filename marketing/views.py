from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import EmailSignupForm
from .models import EmailSignup


def email_list_signup(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email_signup_qs = EmailSignup.objects.filter(email=form.instance.email)
            if email_signup_qs.exists():
                messages.info(request, "You are already subscribed")
            else:
                form.save()
                messages.success(request, "You are successfully subscribed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
