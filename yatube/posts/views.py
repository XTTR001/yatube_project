from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from posts.models import Group, Post


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

