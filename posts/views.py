from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from taggit.models import Tag

from .forms import PostForm
from .models import Post, PostBookmark
from accounts.models import Profile


@login_required
def follow_profile(request):
    
    my_profile = Profile.objects.get(user=request.user)
    pk = request.GET.get('profile_pk')
    obj = Profile.objects.get(pk=pk)

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

    posts = Post.objects.order_by('-created_at')

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


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'home.html', context)


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
