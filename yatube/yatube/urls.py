from django.contrib import admin
from django.urls import include, path

from posts.apps import PostsConfig
from about.apps import AboutConfig
from users.apps import UsersConfig

urlpatterns = [
    path('', include('posts.urls', namespace=PostsConfig.name)),
    path('about/', include('about.urls', namespace=AboutConfig.name)),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace=UsersConfig.name)),
    path('auth/', include('django.contrib.auth.urls')),
]
