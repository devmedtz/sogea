from django.shortcuts import render
from django.db.models import Sum

from posts.models import Post


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
