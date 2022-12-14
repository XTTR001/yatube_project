from django.contrib import admin

from posts.models import Group, Post
from yatube.admin import BaseAdmin


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group',)


@admin.register(Group)
class GroupAdmin(BaseAdmin):
    list_display = ('pk', 'title', 'slug')
    search_fields = ('title', 'slug')
