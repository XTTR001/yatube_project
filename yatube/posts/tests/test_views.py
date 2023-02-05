from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = mixer.blend('posts.Group')

        cls.user = User.objects.create_user(username='auth')

        cls.post = mixer.blend('posts.Post', author=cls.user, group=cls.group)

    def setUp(self) -> None:
        self.guest_client = Client()
        self.user = PostPagesTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_temlate(self):
        """URL-адрес использует соответствующий шаблон."""
        pages_templates_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPagesTests.post.group.slug},
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': PostPagesTests.user.username},
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'pk': PostPagesTests.post.pk},
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'pk': PostPagesTests.post.pk},
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html'
        }

        for reverse_name, template in pages_templates_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_posts_list_pages_show_correct_context(self):
        urls = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': PostPagesTests.post.group.slug},
            ),
            reverse(
                'posts:profile',
                kwargs={'username': PostPagesTests.user.username},
            )
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.text, PostPagesTests.post.text)
                self.assertEqual(
                    first_object.author,
                    PostPagesTests.post.author,
                )
                self.assertEqual(
                    first_object.group,
                    PostPagesTests.post.group,
                )

    def test_post_detail_pages_show_correct_context(self):
        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'pk': PostPagesTests.post.pk}),
        )
        self.assertEqual(
            response.context['post'].text,
            PostPagesTests.post.text,
        )
        self.assertEqual(
            response.context['post'].author,
            PostPagesTests.post.author,
        )
        self.assertEqual(
            response.context['post'].group,
            PostPagesTests.post.group,
        )

    def test_create_post_pages_show_correct_context(self):
        urls = [
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'pk': PostPagesTests.post.pk})
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField

        }
        for url in urls:
            response = self.authorized_client.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)

    def test_create_post_appears_on_main_page(self):
        pass


class PaginatorPostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        fake_post_count = 15

        super().setUpClass()

        cls.group = Group.objects.create(
            title='какая то тестовая группа',
            description='какоето описание',
            slug='kakaya-to-testovaya-gruppa',
        )

        cls.user = User.objects.create_user(username='auth')
        cls.posts = [
            Post.objects.create(
                author=cls.user,
                text=f'Тестовый постkajsndakjsdna;jkdsnas;dkjnasdlkjn{post}',
                group=cls.group
            ) for post in range(fake_post_count)]

    def setUp(self) -> None:
        self.user = PaginatorPostViewsTest.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_list_pages_contains_ten_records(self):
        urls = [
            reverse('posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': PaginatorPostViewsTest.posts[0].group.slug}
            ),
            reverse(
                'posts:profile',
                kwargs={'username': PaginatorPostViewsTest.user.username}
            )
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(
                    len(response.context['page_obj']),
                    settings.PAGE_SIZE,
                )
