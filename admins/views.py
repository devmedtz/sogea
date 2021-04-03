from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from datetime import datetime

from posts.models import Post

User = get_user_model()


@login_required
def admin_dashboard(request):

    approved_posts = Post.objects.filter(status='Approved').count()
    pending_posts = Post.objects.filter(status='Pending').count()
    total_user = User.objects.filter(is_active=True).count()

    total_post_viewer = Post.objects.filter(status='Approved').aggregate(total=Sum('view_count'))

    context = {
        'approved_posts':approved_posts,
        'pending_posts':pending_posts,
        'total_user':total_user,
        'total_post_viewer':total_post_viewer,
    }

    template_name = 'admins/admin_dashboard.html'

    return render(request, template_name, context)


@login_required
def pending_posts(request):

    posts = Post.objects.filter(status='Pending').order_by('-created_at')

    context = {
        'posts':posts,
    }
    template_name = 'admins/pending_posts.html'
    return render(request, template_name, context)


@login_required
def approved_posts(request):

    posts = Post.objects.filter(status='Approved').order_by('-created_at')

    context = {
        'posts':posts,
    }
    template_name = 'admins/approved_posts.html'
    return render(request, template_name, context)


@login_required
def approve_pending_posts(request, slug):

    Post.objects.filter(slug=slug).update(
        status='Approved',
        published_date=datetime.now()
        )

    return redirect('admins:pending_posts')

