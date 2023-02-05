from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from posts.models import Post

User = get_user_model()


class PostCreateAndEditFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.auth = Client()
        cls.auth.force_login(cls.user)

    def test_create_post(self) -> None:
        group = mixer.blend('posts.Group')

        form_data = {
            'text': 'Какой то текст из теста',
            'group': group.id,
        }

        response = self.auth.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}
        ))
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().text, form_data['text'])
        self.assertEqual(Post.objects.get().group.id, form_data['group'])
        self.assertEqual(Post.objects.get().author, self.user)

    def test_create_post_by_anon(self) -> None:
        group = mixer.blend('posts.Group')

        form_data = {
            'text': 'Какой то текст из теста',
            'group': group.id,
        }

        Client().post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), 0)

    def test_edit_post(self) -> None:
        post = mixer.blend('posts.Post', author=self.user)
        group = mixer.blend('posts.Group')

        form_data = {
            'text': f'{post.text} добавили текста',
            'group': group.id
        }

        self.auth.post(
            reverse(
                'posts:post_edit',
                kwargs={'pk': post.pk}
            ),
            data=form_data
        )

        self.assertNotEqual(
            Post.objects.get(pk=post.pk).text,
            post.text
        )

    def test_edit_post_by_anon(self) -> None:
        post = mixer.blend('posts.Post', author=self.user)
        group = mixer.blend('posts.Group')

        form_data = {
            'text': f'{post.text} добавили текста',
            'group': group.id
        }

        Client().post(
            reverse(
                'posts:post_edit',
                kwargs={'pk': post.pk}
            ),
            data=form_data
        )

        self.assertEqual(
            Post.objects.get(pk=post.pk).text,
            post.text
        )

    def test_edit_post_by_not_author(self) -> None:
        post = mixer.blend('posts.Post', author=self.user)
        group = mixer.blend('posts.Group')

        form_data = {
            'text': f'{post.text} добавили текста',
            'group': group.id
        }

        not_author = User.objects.create_user(username='Anton')
        auth = Client()
        auth.force_login(not_author)
        auth.post(
            reverse(
                'posts:post_edit',
                kwargs={'pk': post.pk}
            ),
            data=form_data
        )

        self.assertEqual(
            Post.objects.get(pk=post.pk).text,
            post.text
        )
