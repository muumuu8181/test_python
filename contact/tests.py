from django.test import TestCase
from django.urls import reverse
from .models import ContactMessage

class ContactTest(TestCase):
    def test_contact_page_status_code(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        })
        # Check for redirect (success)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='john@example.com').exists())
