from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from taggit.models import Tag

from .forms import PostForm
from .models import Post, PostBookmark


def create_post(request):

    posts = Post.objects.order_by('-created_at')
    print('posts:',posts)
    # Show most common tags 
    common_tags = Post.tags.most_common()[:4]
    print('comon_tags:',common_tags)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            post_obj = form.save(commit=False)
            post_obj.author_id = request.user.id
            post_obj.save()

            form.save_m2m() #for save tags

            messages.success(
                request, 'Your Post Has Been Created', extra_tags='alert alert-success')

            return redirect(to='posts:create_post')
        else:
            messages.error(request, 'Errors occurred',extra_tags='alert alert-danger')
    else:
        form = PostForm()

    template_name = 'posts/create_post.html'

    context = {
        'posts':posts,
        'common_tags':common_tags,
        'form':form,
    }

    return render(request, template_name, context)





def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'home.html', context)


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
