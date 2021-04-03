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

    posts_list = Post.objects.filter(status='Approved').exclude(featured=True).order_by('-published_date')

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

    print(one_day_ago)

    posts_list = Post.objects.filter(published_date__lte=one_day_ago, status='Approved').exclude(featured=True).order_by('-published_date')

    print('posts_list:',posts_list)

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

    posts_list = Post.objects.filter(published_date__lte=one_week_ago, status='Approved').exclude(featured=True).order_by('-published_date')

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

    posts_list = Post.objects.filter(published_date__lte=one_month_ago, status='Approved').exclude(featured=True).order_by('-published_date')
   
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

    posts_list = Post.objects.filter(published_date__lte=one_year_ago, status='Approved').exclude(featured=True).order_by('-published_date')
   
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

    if not request.user == post.author:
        post.view_count += 1
        post.save()

    post_bookmarks = PostBookmark.objects.filter(post=post).count()

    if request.user.is_authenticated:
        post_state = PostBookmark.objects.filter(user=request.user, post=post)
        like_state = post.likes.filter(id=request.user.id)


        following = post.author.profile.following.count()
        followers = Profile.objects.filter(following=post.author).count()

        #follow
  
        view_profile = Profile.objects.get(pk=post.author.profile.pk)
 
        my_profile = Profile.objects.get(user=request.user)
  

        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False

        context = {
            'followers':followers,
            'following':following,
            'post_state':post_state,
            'like_state':like_state, 
            'follow':follow, 
            'profile':my_profile,
            'post':post,
            'post_bookmarks':post_bookmarks,
        }

        template_name = 'main/post_detail.html'

        return render(request, template_name, context)

    context = {
        'post':post,
        'post_bookmarks':post_bookmarks,
    }

    template_name = 'main/post_detail.html'

    return render(request, template_name, context)


def code_of_conduct(request):

    context = {}
    template_name = 'main/pages/code_of_conduct.html'
    return render(request, template_name, context)

def terms_of_use(request):

    context = {}
    template_name = 'main/pages/terms_of_use.html'
    return render(request, template_name, context)

def privacy_policy(request):

    context = {}
    template_name = 'main/pages/privacy_policy.html'
    return render(request, template_name, context)

def contacts(request):

    context = {}
    template_name = 'main/pages/contacts.html'
    return render(request, template_name, context)

def about(request):

    context = {}
    template_name = 'main/pages/about.html'
    return render(request, template_name, context)

def FAQ(request):

    context = {}
    template_name = 'main/pages/faq.html'
    return render(request, template_name, context)
