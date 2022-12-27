from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm
from posts.models import Group, Post, User


def get_page_obj(request, objects, items_per_page):
    paginator = Paginator(objects, items_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.select_related(
        'author',
        'group',
    )

    page_obj = get_page_obj(request, post_list, 10)

    return render(request, 'posts/index.html', context={'page_obj': page_obj})


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related(
        'author',
    )

    page_obj = get_page_obj(request, post_list, 10)

    return render(
        request,
        'posts/group_list.html',
        context={'page_obj': page_obj, 'group': group},
    )


def profile(request, username) -> HttpResponse:
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related(
        'group'
    )

    page_obj = get_page_obj(request, post_list, 10)

    return render(
        request,
        'posts/profile.html',
        context={'page_obj': page_obj, 'author': author}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related(
        'author',
        'group',
    ), pk=post_id)
    author_id = post.author.id

    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
            'author_posts_count': Post.objects.filter(
                author=author_id,
            ).count()
        }
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None)

    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect(f'/profile/{post.author.username}/')


@login_required
def post_edit(request, post_id):

    post = get_object_or_404(Post.objects.select_related(
        'author',
        'group',
    ), pk=post_id)

    if request.user != post.author:
        return redirect(f'/posts/{post_id}/')

    form = PostForm(instance=post, data=request.POST or None)

    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {'form': form, 'is_edit': True, 'post_id': post_id})

    form.save()
    return redirect(f'/posts/{post_id}/')
