from django.contrib import admin
from django.urls import include, path

from posts.apps import PostsConfig
from about.apps import AboutConfig

urlpatterns = [
    path('', include('posts.urls', namespace=PostsConfig.name)),
    path('about/', include('about.urls', namespace=AboutConfig.name)),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
