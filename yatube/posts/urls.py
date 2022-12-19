from django.urls import path

from posts.apps import PostsConfig
from posts.views import group_posts, index

app_name = PostsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('group/<slug:slug>', group_posts, name='group_list'),
]
