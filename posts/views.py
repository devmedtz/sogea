from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
import json
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.generic import View
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count, Q

from .forms import PostForm
from .models import Post, PostBookmark
from accounts.models import Profile


def ajax_authenticate_user(request):

    if request.user.is_authenticated:
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})


@login_required
def save_likes(request):

    if request.method =="POST":
        print('in request')
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            content_id=request.POST.get("content_id",None)
            print('content_id:',content_id)
            content=get_object_or_404(Post, pk=content_id)
            if content.likes.filter(id=request.user.id): #already liked the content
                content.likes.remove(request.user) #remove user from likes 
                liked=False
            else:
                content.likes.add(request.user) 
                liked=True

            context = {"likes_count":content.total_likes,"liked":liked,"content_id":content_id}

            return HttpResponse(json.dumps(context), content_type='application/json')

        already_liked=[]
        id=request.user.id
        for content in posts_list:
            if(content.likes.filter(id=id).exists()):
                already_liked.append(content.id)

        context = {"contents":contents,"already_liked":already_liked}
    return HttpResponse('success')


@login_required
def follow_profile(request):
    
    my_profile = Profile.objects.get(user=request.user)

    pk = request.GET.get('profile_pk')

    obj = Profile.objects.get(pk=pk)

    if obj.user == request.user:
        print('cant follow your self')
        return JsonResponse({'status': 'none'})
    else:
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            return JsonResponse({'bool': False})
        else:
            my_profile.following.add(obj.user)
            return JsonResponse({'bool': True})


@login_required
def create_edit_post(request, id=None):

    user = request.user

    if id:
        obj = get_object_or_404(Post, id=id)
        if obj.author != user:
            raise PermissionDenied()
    else:
        obj = Post(author=user)

    posts = Post.objects.order_by('-published_date')

    # Show most common tags 
    common_tags = Post.tags.most_common()[:4]


    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():

            post_obj = form.save(commit=False)
            post_obj.author_id = request.user.id
            post_obj.save()

            form.save_m2m() #for save tags

            if id:
                messages.success(
                request, 'Your Post Has Been Updated', extra_tags='alert alert-success')
            else:
                messages.success(
                request, 'Your Post Has Been Created', extra_tags='alert alert-success')
                
            return redirect(to='dashboard:dashboard')
        else:
            messages.error(request, 'Errors occurred',extra_tags='alert alert-danger')
    else:
        form = PostForm(instance=obj)

    template_name = 'posts/create_post.html'

    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }

    return render(request, template_name, context)

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user == post.author:
        post.delete()
    else: 
        raise PermissionDenied()

    return redirect(reverse("dashboard:dashboard"))


@login_required
def save_post_bookmark(request):

    if request.method == 'POST':
        post_id = request.POST['postID']
        post = Post.objects.get(id=post_id)
        user = request.user

        post_bookmark = PostBookmark.objects.filter(
            post=post, user=user)
        if post_bookmark.exists():
            post_bookmark.delete()
            return JsonResponse({'bool': False})
        else:
            PostBookmark.objects.create(
                post=post,
                user=user
            )
            return JsonResponse({'bool': True})


def search(request):
    queryset = Post.objects.filter(status='Approved').order_by('-published_date')

    if 'query' in request.GET: 
        query = request.GET.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()

    
    # Show most common tags 
    common_tags = Post.tags.most_common()[:5]

    context = {
        'posts_list': queryset,
        'values':request.GET,
        'common_tags':common_tags,
    }
    return render(request, 'posts/search_results.html', context)


def post_tag_list(request, tag):

    queryset = Post.objects.filter(status='Approved',tags__name__icontains=tag).order_by('-published_date')

        # Show most common tags 
    common_tags = Post.tags.most_common()[:5]

    context = {
        'posts_list': queryset,
        'tag':tag,
        'common_tags':common_tags,
    }

    template_name = 'posts/tags_post_list.html'

    return render(request, template_name, context)