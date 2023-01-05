from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from yatube.utils import truncatechars

User = get_user_model()


class Group(models.Model):
    title_max_lenght = 200

    title = models.CharField(
        max_length=title_max_lenght, verbose_name='название'
    )
    slug = models.SlugField(unique=True, verbose_name='slug')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self) -> str:
        return truncatechars(self.title)


class Post(models.Model):
    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='дата публикации'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='группа',
    )

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self) -> str:
        return truncatechars(self.text)
