from django.apps import AppConfig
from django.conf import settings


class PostsConfig(AppConfig):
    default_auto_field = settings.DEFAULT_BIG_FIELD
    name = 'posts'
    verbose_name = 'публикации'
