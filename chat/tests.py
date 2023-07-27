from django.test import TestCase, Client
from django.urls import reverse

class CoreViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        url = reverse('core:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_about_view(self):
        url = reverse('core:about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
