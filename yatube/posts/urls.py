from django.urls import path

from posts.views import index, group_posts
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('group/<slug:slug>', group_posts, name='group_list'),
]
