from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm
from posts.models import Group, Post, User
from yatube.utils import get_page_obj


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related('author', 'group',)

    page = get_page_obj(request, posts)

    return render(request, 'posts/index.html', context={'page_obj': page})


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author',)

    page = get_page_obj(request, posts)

    return render(
        request,
        'posts/group_list.html',
        context={'page_obj': page, 'group': group},
    )


def profile(request: HttpRequest, username: str) -> HttpResponse:
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')

    page = get_page_obj(request, posts)

    return render(
        request,
        'posts/profile.html',
        context={'page_obj': page, 'author': author},
    )


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related('author', 'group',), pk=pk
    )
    author_id = post.author.id

    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
        },
    )


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None)

    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})

    form.instance.author = request.user
    form.save()
    return redirect('posts:profile', username=request.user.username)


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related('author', 'group',), pk=pk
    )

    if request.user != post.author:
        return redirect('posts:post_detail', pk=pk)

    form = PostForm(instance=post, data=request.POST or None)

    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {'form': form, 'is_edit': True, 'post_id': pk},
        )

    form.save()
    return redirect('posts:post_detail', pk=pk)
