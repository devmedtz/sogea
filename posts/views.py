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

from .forms import PostForm,CommentForm, ReplyForm
from .models import Post, PostBookmark, Comment, Reply
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


def search(request):
    queryset = Post.objects.filter(status='Approved').order_by('-created_at')

    if 'query' in request.GET: 
        query = request.GET.get('query')
        if query:
            queryset = queryset.filter(title__icontains=query)

    context = {
        'posts_list': queryset,
        'values':request.GET,
    }
    return render(request, 'posts/search_results.html', context)



@method_decorator(login_required, name='dispatch')
class CommentCreate(View):
    data = dict()
    template_name = "comments/comment_reply_partial.html"

    def post(self, request, post_pk):
        comment_text = request.POST.get("text")
        author = request.user.profile
        post = get_object_or_404(Post, pk=post_pk)
        comment = Comment(post=post, author=author, text=comment_text)
        comment.save()
        html_content = render_to_string(self.template_name, {
            "comment": comment,
            'profile': request.user.profile
        })
        self.data['successful'] = True
        self.data['html_content'] = html_content
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class CommentUpdate(View):
    form_class = CommentForm
    form_template = "comments/comment_update_partial.html"
    template_name = "comments/comment_partial.html"
    data = dict()

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = self.form_class(instance=comment)
        html_form = render_to_string(self.form_template, {
            "comment": comment,
            "form": form
        }, request=request)
        self.data['successful'] = True
        self.data['html_form'] = html_form
        return JsonResponse(self.data)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = self.form_class(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            html_content = render_to_string(self.template_name, {"comment": comment, 'profile': request.user.profile})
            self.data['successful'] = True
            self.data['html_content'] = html_content
            self.data['pk'] = pk
            return JsonResponse(self.data)
        else:
            self.data['successful'] = False
            html_form = render_to_string(self.form_template, {'form': form, 'comment': comment})
            self.data['html_form'] = html_form
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class CommentDelete(View):
    data = dict()

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            self.data['successful'] = True
            self.data['message'] = "Comment Deleted"
            self.data['pk'] = pk
        except Comment.DoesNotExist:
            self.data['successful'] = False
            self.data['message'] = "comment not found"
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyCreate(View):
    data = dict()
    template_name = "comments/reply_partial.html"

    def post(self, request, comment_pk):
        reply_text = request.POST.get("reply-text")
        author = request.user.profile

        comment = Comment.objects.get(pk=comment_pk)
        reply = Reply(comment=comment, author=author, text=reply_text)
        reply.save()

        html_content = render_to_string(self.template_name, {
            "reply": reply,
            'profile': request.user.profile
        })
        self.data['successful'] = True
        self.data['html_content'] = html_content
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyCreateold(View):
    template_name = "comments/reply_partial.html"
    form_template = "comments/reply_partial_create.html"
    form_class = ReplyForm
    data = dict()

    def get(self, request, comment_pk=None):
        form = self.form_class()
        try:
            comment = Comment.objects.get(pk=comment_pk)
            html_form = render_to_string(self.form_template, {'form': form, 'comment': comment}, request=request)
            self.data['html_form'] = html_form
            self.data['html_form'] = html_form
            self.data['successful'] = True
        except Comment.DoesNotExist:
            self.data['successful'] = False

        return JsonResponse(self.data)

    def post(self, request, comment_pk=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            try:
                comment = Comment.objects.get(pk=comment_pk)
                reply.comment = comment
                reply.author = request.user.profile
                reply.save()
                self.data['successful'] = True
                self.data['html_content'] = render_to_string(self.template_name, {'reply': reply,'profile': request.user.profile}, request=request)
                self.data['pk'] = comment_pk
            except Comment.DoesNotExist:
                self.data['successful'] = False
        else:
            self.data['successful'] = False
            self.data['html_form'] = render_to_string(self.form_template, {'form': form})
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyUpdate(View):
    form_class = ReplyForm
    data = dict()
    template_name = "comments/reply_partial.html"
    form_template = "comments/reply_partial_update.html"

    def get(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
            form = self.form_class(instance=reply)
            html_form = render_to_string(self.form_template, {'form': form, 'reply': reply}, request=request)
            self.data['html_form'] = html_form
            self.data['successful'] = True
        except Reply.DoesNotExist:
            self.data['successful'] = False
        return JsonResponse(self.data)

    def post(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
            form = self.form_class(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                self.data['successful'] = True
                self.data['html_content'] = render_to_string(self.template_name, {"reply": reply,
                                                                                  'profile': request.user.profile},
                                                             request=request)
                self.data['pk'] = pk
            else:
                self.data['successful'] = False
                self.data['html_form'] = render_to_string(self.form_template, {'form': form, 'reply': reply},
                                                          request=request)
        except Reply.DoesNotExist:
            self.data['successful'] = False

        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyDelete(View):
    data = dict()

    def get(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
            reply.delete()
            self.data['successful'] = True
            self.data['message'] = "Comment Deleted"
            self.data['pk'] = pk
        except Reply.DoesNotExist:
            self.data['successful'] = False
            self.data['message'] = "comment not found"
        return JsonResponse(self.data)