from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from posts.models import Post
from accounts.models import Profile
from .forms import ProfileForm


def dashboard(request):

    user = request.user

    posts = Post.objects.filter(author=user).order_by('-created_at')

    post_views = posts.aggregate(total=Sum('view_count'))

    context = {
        'posts':posts,
        'post_views':post_views,
        'total_post':posts.count(),
    }

    template_name = 'dashboard/index.html'

    return render(request, template_name, context)

@login_required
def profile_update(request, id):

    profile = get_object_or_404(Profile, user_id=id)

    if profile.user != request.user: 
        raise PermissionDenied()

    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()

        return redirect(reverse("dashboard:profile_update", kwargs={
            'id': id
        }))
        messages.success(request, "You are successfully update profile")
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form':form
    }

    template_name = 'dashboard/profile_update.html'

    return render(request, template_name, context)
