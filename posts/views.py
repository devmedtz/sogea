from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from taggit.models import Tag

from .forms import PostForm
from .models import Post


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


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, 'detail.html', context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'home.html', context)
