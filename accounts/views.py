from allauth.account.views import LoginView, SignupView

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.forms import SignUpForm, MyAuthForm
from accounts.models import CustomUser, Profile
from posts.models import Post


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


def profile_detail(request, username):

    profile = get_object_or_404(Profile, user__username=username)

    posts_list = Post.objects.filter(status='Approved', author=profile.user).exclude(featured=True).order_by('-created_at')

    #follow
    following = profile.following.count()
    followers = Profile.objects.filter(following=profile.user).count()

    if request.user.is_authenticated:
        my_profile = Profile.objects.get(user=request.user)

        if profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False

        context = {
            'profile':profile,
            'posts_list':posts_list,
            'following':following,
            'followers':followers,
            'follow':follow
            }

        template_name = 'profile/profile_detail.html'

        return render(request, template_name, context)


    context = {
        'profile':profile,
        'posts_list':posts_list,
        'following':following,
        'followers':followers,
    }

    template_name = 'profile/profile_detail.html'

    return render(request, template_name, context=context)