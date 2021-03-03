# from django.contrib.auth.views import LoginView, LogoutView

from allauth.account.views import LoginView, SignupView

from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.forms import SignUpForm, MyAuthForm
from accounts.models import CustomUser


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = MyAuthForm

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        elif self.request.user.is_admin:
            return reverse('admins:dashboard')
        else:
            return f'/admin/'


class Signup(LoginRequiredMixin, UserPassesTestMixin, SignupView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if request.method == 'POST':
            if form.is_valid():
                user = form.save()
                user.save()

                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True

