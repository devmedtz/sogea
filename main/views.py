from django.shortcuts import render, get_object_or_404, Http404, redirect
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import HttpResponse
from datetime import datetime, timedelta

from posts.models import Post,PostBookmark
from accounts.models import Profile
from marketing.forms import EmailSignupForm


def homepage(request):

    template_name = 'main/index.html'

    posts_list = Post.objects.filter(status='Approved').exclude(featured=True).order_by('-created_at')

    try:
        p_ft = Post.objects.get(featured=True)
        common_tags = Post.tags.most_common()[:4]
    except Post.DoesNotExist:
        p_ft = None
        common_tags = None

   
    context = {
        'posts_list':posts_list,
        'form':EmailSignupForm(),
        'common_tags':common_tags,
        'p_ft':p_ft,
    }

    return render(request, template_name, context=context)


def yesterday_posts(request):

    template_name = 'main/index.html'

    one_day_ago = datetime.today() - timedelta(days=1)

    posts_list = Post.objects.filter(created_at__lte=one_day_ago, status='Approved').exclude(featured=True).order_by('-created_at')

    try:
        p_ft = Post.objects.get(featured=True)
        common_tags = Post.tags.most_common()[:4]
    except Post.DoesNotExist:
        p_ft = None
        common_tags = None

    context = {
        'posts_list':posts_list,
        'form':EmailSignupForm(),
        'common_tags':common_tags,
        'p_ft':p_ft,
    }

    return render(request, template_name, context=context)


def weekly_posts(request):

    template_name = 'main/index.html'

    one_week_ago = datetime.today() - timedelta(days=7)

    posts_list = Post.objects.filter(created_at__lte=one_week_ago, status='Approved').exclude(featured=True).order_by('-created_at')

    try:
        p_ft = Post.objects.get(featured=True)
        common_tags = Post.tags.most_common()[:4]
    except Post.DoesNotExist:
        p_ft = None
        common_tags = None

    context = {
        'posts_list':posts_list,
        'form':EmailSignupForm(),
        'common_tags':common_tags,
        'p_ft':p_ft,
    }

    return render(request, template_name, context=context)


def monthly_posts(request):

    template_name = 'main/index.html'

    one_month_ago = datetime.today() - timedelta(days=30)

    posts_list = Post.objects.filter(created_at__lte=one_month_ago, status='Approved').exclude(featured=True).order_by('-created_at')
   
    try:
        p_ft = Post.objects.get(featured=True)
        common_tags = Post.tags.most_common()[:4]
    except Post.DoesNotExist:
        p_ft = None
        common_tags = None

    context = {
        'posts_list':posts_list,
        'form':EmailSignupForm(),
        'common_tags':common_tags,
        'p_ft':p_ft,
    }

    return render(request, template_name, context=context)


def yearly_posts(request):

    template_name = 'main/index.html'

    one_year_ago = datetime.today() - timedelta(days=365)

    posts_list = Post.objects.filter(published_date__lte=one_year_ago, status='Approved').exclude(featured=True).order_by('-created_at')
   
    try:
        p_ft = Post.objects.get(featured=True)
        common_tags = Post.tags.most_common()[:4]
    except Post.DoesNotExist:
        p_ft = None
        common_tags = None

    context = {
        'posts_list':posts_list,
        'form':EmailSignupForm(),
        'common_tags':common_tags,
        'p_ft':p_ft,
    }

    return render(request, template_name, context=context)


def post_detail(request, post_slug):

    post = get_object_or_404(Post, slug=post_slug)
    post.view_count += 1
    post.save()
 
    post_bookmarks = PostBookmark.objects.filter(post=post).count()

    if request.user.is_authenticated:
        post_state = PostBookmark.objects.filter(user=request.user, post=post)
        like_state = post.likes.filter(id=request.user.id)

        #follow
  
        view_profile = Profile.objects.get(pk=post.author.profile.pk)
 
        my_profile = Profile.objects.get(user=request.user)
  

        if view_profile.user in my_profile.following.all():
            follow = True
        elif view_profile == my_profile:
            follow = 'hide'
        else:
            follow = False

        context = {'post':post,'post_state':post_state,'post_bookmarks':post_bookmarks,'like_state':like_state, 'follow':follow}

        template_name = 'main/post_detail.html'

        return render(request, template_name, context)

    context = {
        'post':post,
        'post_bookmarks':post_bookmarks,
    }

    template_name = 'main/post_detail.html'

    return render(request, template_name, context)
