from django.urls import path

import posts.views
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', posts.views.index, name='index'),
    path('group/<slug:slug>', posts.views.group_posts, name='group_list'),
]
