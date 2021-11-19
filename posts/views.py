from .forms import CreatePostModelForm, CommentModelForm
from profiles.models import Profile
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, HttpResponse

# Create your views here.
from.models import Post, Comment, Like


def post_create_comment_and_list_view(request):

    user = request.user
    obj = Profile.objects.get(user=user)
    posts = Post.objects.select_related('author').all()
    post_form = CreatePostModelForm()
    comment_form = CommentModelForm()
    if request.method == 'POST' and 'post_btn' in request.POST:
        post_form = CreatePostModelForm(
            request.POST, request.FILES)
        if post_form.is_valid():
            image = post_form.cleaned_data.get('image')
            data = post_form.save(commit=False)
            data.author = obj
            data.image = image
            data.save()
            post_form = CreatePostModelForm()
    elif request.method == 'POST' and 'comment_btn' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = comment_form.save(commit=False)
            comment.user = obj
            comment.post = post
            comment.save()
            comment_form = CommentModelForm()

    context = {'user': user, 'posts': posts, 'obj': obj,
               'post_form': post_form, 'comment_form': comment_form}
    return render(request, 'posts/index.html', context)


def like_unlike_view(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        user = Profile.objects.get(user=request.user)
        if user in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        post.save()
        like.save()
    return redirect('posts:post-list-view')
