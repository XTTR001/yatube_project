from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author = User.objects.create_user(username='anton')
        cls.group = mixer.blend('posts.Group')
        cls.post = mixer.blend(
            'posts.Post', author=cls.author, group=cls.group
        )

        cls.anon = Client()
        cls.auth = Client()
        cls.auth.force_login(cls.user)
        cls.auth_author = Client()
        cls.auth_author.force_login(cls.author)

        cls.urls = {
            'index': reverse('posts:index'),
            'group': reverse('posts:group_list', args=(cls.group.slug,)),
            'profile': reverse('posts:profile', args=(cls.author.username,)),
            'post_detail': reverse('posts:post_detail', args=(cls.post.pk,)),
            'post_create': reverse('posts:post_create'),
            'post_edit': reverse('posts:post_edit', args=(cls.post.pk,)),
            'missing': '/unexisting_url/',
        }

    def test_http_statuses(self) -> None:
        httpstatuses = (
            (self.urls.get('index'), HTTPStatus.OK, self.anon),
            (self.urls.get('group'), HTTPStatus.OK, self.anon),
            (self.urls.get('profile'), HTTPStatus.OK, self.anon),
            (self.urls.get('post_detail'), HTTPStatus.OK, self.anon),
            (self.urls.get('post_create'), HTTPStatus.FOUND, self.anon),
            (self.urls.get('post_create'), HTTPStatus.OK, self.auth),
            (self.urls.get('post_edit'), HTTPStatus.FOUND, self.anon),
            (self.urls.get('post_edit'), HTTPStatus.FOUND, self.auth),
            (self.urls.get('post_edit'), HTTPStatus.OK, self.auth_author),
            (self.urls.get('missing'), HTTPStatus.NOT_FOUND, self.anon),
        )
        for url, status, user in httpstatuses:
            with self.subTest(user=user):
                self.assertEqual(user.get(url).status_code, status)

    def test_templates(self) -> None:
        templates = (
            (self.urls.get('index'), 'posts/index.html', self.anon),
            (self.urls.get('group'), 'posts/group_list.html', self.anon),
            (self.urls.get('profile'), 'posts/profile.html', self.anon),
            (
                self.urls.get('post_detail'),
                'posts/post_detail.html',
                self.anon,
            ),
            (
                self.urls.get('post_create'),
                'posts/create_post.html',
                self.auth_author,
            ),
            (
                self.urls.get('post_edit'),
                'posts/create_post.html',
                self.auth_author,
            ),
        )

        for url, template, user in templates:
            with self.subTest(user=user):
                self.assertTemplateUsed(user.get(url), template)

    def test_redirects(self) -> None:
        redirects = (
            (
                self.urls.get('post_create'),
                f'{reverse("users:login")}?next=/create/',
                self.anon,
            ),
            (
                self.urls.get('post_edit'),
                reverse('posts:post_detail', args=(self.post.pk,)),
                self.auth,
            ),
        )

        for url, redirect, user in redirects:
            with self.subTest(user=user):
                self.assertRedirects(user.get(url, follow=True), redirect)
