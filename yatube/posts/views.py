from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from posts.models import Group, Post


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related('author', 'group')[
        : settings.POSTS_PAGE_LIMIT
    ]

    return render(request, 'posts/index.html', context={'posts': posts})


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')[: settings.POSTS_PAGE_LIMIT]
    return render(
        request,
        'posts/group_list.html',
        context={'posts': posts, 'group': group},
    )
