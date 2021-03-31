from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()

@login_required
def admin_dashboard(request):

    approved_posts = Post.objects.filter(status='Approved').count()
    pending_posts = Post.objects.filter(status='Pending').count()
    total_user = User.objects.filter(is_active=True).count()

    # post_views = posts.aggregate(total=Sum('view_count'))

    # profile = Profile.objects.get(user=user)

    # following = profile.following.count()

    # followers = Profile.objects.filter(following=profile.user).count()

    context = {
        'approved_posts':approved_posts,
        'pending_posts':pending_posts,
        'total_user':total_user
    }

    template_name = 'admins/admin_dashboard.html'

    return render(request, template_name, context)
