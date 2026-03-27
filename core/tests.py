from django.test import TestCase
from django.urls import reverse
from .models import Page

class PageModelTest(TestCase):
    def test_string_representation(self):
        page = Page(title="About Us")
        self.assertEqual(str(page), "About Us")

class PageViewTest(TestCase):
    def setUp(self):
        self.page = Page.objects.create(
            title="About Us",
            slug="about-us",
            content="This is the about page.",
            status="published"
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_page_detail_view(self):
        response = self.client.get(reverse('page_detail', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About Us")
        self.assertContains(response, "This is the about page.")
