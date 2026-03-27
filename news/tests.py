from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(
            title="First Post",
            slug="first-post",
            author=self.user,
            content="This is the first post.",
            status="published"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.post), "First Post")

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First Post")

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the first post.")
