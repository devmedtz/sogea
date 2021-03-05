from django.shortcuts import render, get_object_or_404, Http404
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Post


def homepage(request):
    posts_list = Post.objects.all().order_by('-created_at')
   
    try:
        p_ft = Post.objects.get(featured=1)
        common_tags = Post.tags.most_common()[:4]
    except:
        pass
   

    template_name = 'main/index.html'

    context = {
        'posts_list':posts_list,
        'p_ft':p_ft,
        'common_tags':common_tags,
    }

    return render(request, template_name, context=context)



def post_detail(request, post_slug):

    try:
        post = get_object_or_404(Post, slug=post_slug)
        post.view_count += 1
        post.save()
    except ObjectDoesNotExist:
        raise Http404

    context = {
        'post':post,
    }

    template_name = 'main/post_detail.html'

    return render(request, template_name, context)