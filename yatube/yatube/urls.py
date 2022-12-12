from django.contrib import admin
from django.urls import include, path

from posts.apps import PostsConfig

urlpatterns = [
    path('', include('posts.urls', namespace=PostsConfig.name)),
    path('group/', include('posts.urls', namespace=PostsConfig.name)),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]
