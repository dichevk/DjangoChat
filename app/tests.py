from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.views import edit_user, add_user


class EditUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add('user.edit_user')
        self.uuid = str(self.user.pk)

    def test_edit_user_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_user', args=[self.uuid]), data={'some_form_data': 'value'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/chat-admin/')

    def test_edit_user_permission_denied(self):
        self.client.login(username='testuser', password='testpassword')
        self.user.user_permissions.remove('user.edit_user')
        response = self.client.post(reverse('edit_user', args=[self.uuid]), data={'some_form_data': 'value'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/chat-admin/')
        self.assertContains(response, 'You don\'t have access to edit users!')

class AddUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add('user.add_user')

    def test_add_user_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_user'), data={'some_form_data': 'value'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/app-admin/')
        self.assertEqual(User.objects.count(), 2)  # Assuming the user count before the test is 1

    def test_add_user_permission_denied(self):
        self.client.login(username='testuser', password='testpassword')
        self.user.user_permissions.remove('user.add_user')
        response = self.client.post(reverse('add_user'), data={'some_form_data': 'value'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/app-admin/')
        self.assertContains(response, 'Access denied')
