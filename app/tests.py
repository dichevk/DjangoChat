from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.views import edit_user, add_user
from account.forms import EditUserForm, AddUserForm


class EditUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_with_permission = User.objects.create_user(username='user_with_perm', password='testpassword')
        self.user_with_permission.user_permissions.add('user.edit_user')
        self.user_without_permission = User.objects.create_user(username='user_without_perm', password='testpassword')
        self.user_to_edit = User.objects.create_user(username='user_to_edit', password='testpassword')

    def test_edit_user_with_permission(self):
        self.client.login(username='user_with_perm', password='testpassword')
        form_data = {'username': 'new_username', 'email': 'new_email@example.com'}
        response = self.client.post(reverse('edit_user', args=[self.user_to_edit.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/chat-admin/')
        self.assertEqual(User.objects.get(pk=self.user_to_edit.pk).username, 'new_username')
        self.assertEqual(User.objects.get(pk=self.user_to_edit.pk).email, 'new_email@example.com')

    def test_edit_user_without_permission(self):
        self.client.login(username='user_without_perm', password='testpassword')
        form_data = {'username': 'new_username', 'email': 'new_email@example.com'}
        response = self.client.post(reverse('edit_user', args=[self.user_to_edit.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/chat-admin/')
        self.assertEqual(User.objects.get(pk=self.user_to_edit.pk).username, 'user_to_edit')  # No change
        self.assertEqual(User.objects.get(pk=self.user_to_edit.pk).email, '')  # No change

    def test_edit_user_permission_denied(self):
        response = self.client.post(reverse('edit_user', args=[self.user_to_edit.pk]), data={})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/chat-admin/')
        self.assertIn(b"You don't have access to edit users!", response.content)

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
        
    def test_edit_user_invalid_form(self):
        self.client.login(username='user_with_perm', password='testpassword')
        form_data = {'username': '', 'email': 'invalid_email'}  # Invalid form data
        response = self.client.post(reverse('edit_user', args=[self.user_to_edit.pk]), data=form_data)
        self.assertEqual(response.status_code, 200)  # 200 is the status code for form validation error
        self.assertContains(response, 'This field is required.')  # Check if form validation error message is shown
        self.assertNotEqual(User.objects.get(pk=self.user_to_edit.pk).email, 'invalid_email')  # No change due to invalid data

class AddUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_with_permission = User.objects.create_user(username='user_with_perm', password='testpassword')
        self.user_with_permission.user_permissions.add('user.add_user')
        self.user_without_permission = User.objects.create_user(username='user_without_perm', password='testpassword')

    def test_add_user_with_permission(self):
        self.client.login(username='user_with_perm', password='testpassword')
        form_data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'password123'}
        response = self.client.post(reverse('add_user'), data=form_data)
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/app-admin/')
        new_user = User.objects.get(username='new_user')
        self.assertTrue(new_user.is_staff)
        self.assertTrue(new_user.check_password('password123'))

    def test_add_user_without_permission(self):
        self.client.login(username='user_without_perm', password='testpassword')
        form_data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'password123'}
        response = self.client.post(reverse('add_user'), data=form_data)
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/app-admin/')
        self.assertIsNone(User.objects.filter(username='new_user').first())

    def test_add_user_permission_denied(self):
        response = self.client.post(reverse('add_user'), data={})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/app-admin/')
        self.assertIn(b"Access denied", response.content)

    def test_add_user_permission_denied(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('add_user'), data={'some_form_data': 'value'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code
        self.assertEqual(response.url, '/app-admin/')
        self.assertContains(response, 'Access denied')

    def test_add_user_duplicate_username(self):
        self.client.login(username='user_with_perm', password='testpassword')
        form_data = {'username': 'existing_user', 'email': 'new_user@example.com', 'password': 'password123'}
        response = self.client.post(reverse('add_user'), data=form_data)
        self.assertEqual(response.status_code, 200)  # 200 is the status code for form validation error
        self.assertContains(response, 'A user with that username already exists.')  # Check if form validation error message is shown
        self.assertIsNone(User.objects.filter(username='existing_user').first())  # No new user created