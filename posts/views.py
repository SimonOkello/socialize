from django.contrib import messages
from .forms import CreatePostModelForm, CommentModelForm
from profiles.models import Profile, Relationship
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse

# Create your views here.
from.models import Post, Comment, Like


def post_create_comment_and_list_view(request):
    user = request.user
    obj = Profile.objects.get(user=user)
    my_friends = Relationship.objects.accepted_friends(obj)
    print("FRIENDS:", my_friends)
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
               'my_friends': my_friends, 'post_form': post_form,
               'comment_form': comment_form}
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


def edit_post_view(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    obj = get_object_or_404(Post, pk=pk)
    if obj.author == profile:
        post_form = CreatePostModelForm(instance=obj)
        context = {'obj': obj, 'post_form': post_form}
        if request.method == 'POST':
            post_form = CreatePostModelForm(
                request.POST, request.FILES, instance=obj)
            if post_form.is_valid():
                image = post_form.cleaned_data.get('image')
                instance = post_form.save(commit=False)
                instance.author = profile
                instance.image = image
                instance.save()
                messages.success(
                    request, 'Post has been updated!')
                return redirect('posts:post-list-view')
    else:
        messages.warning(request, 'You are not the author of this post')
        return redirect('posts:post-list-view')

    return render(request, 'posts/edit-post.html', context)


def delete_post_view(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    obj = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if obj.author == profile:
            obj.delete()
            messages.success(
                request, 'Post has been deleted!')
            return redirect('posts:post-list-view')
        else:
            messages.error(
                request, 'You need to be the author of the post to delete')
            return redirect('posts:post-list-view')
    else:
        messages.error(request, 'Something went wrong!')
        return redirect('posts:post-list-view')
