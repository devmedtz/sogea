from django.shortcuts import render


from posts.models import Post


def homepage(request):

    posts = Post.objects.all().order_by('-created_at')
    featured = Post.objects.get(featured=True)
    common_tags = Post.tags.most_common()[:4]

    template_name = 'main/index.html'

    context = {
        'posts':posts,
        'featured':featured,
        'common_tags':common_tags,
    }

    return render(request, template_name, context=context)
