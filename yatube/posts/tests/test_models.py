from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from mixer.backend.django import mixer

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = mixer.blend(
            'posts.Post',
            author=mixer.blend(User, username='auth')
        )

    def test_post_model_have_correct_object_name(self):
        self.assertGreaterEqual(
            settings.SHOWTEXT_LENGTH,
            len(self.post.__str__()),
        )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = mixer.blend('posts.Group')

    def test_group_model_have_correct_object_name(self):
        self.assertEqual(
            self.group.title,
            self.group.title.__str__(),
        )
