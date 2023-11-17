from django.test import TestCase
from django.urls import reverse

from authapp.forms import AdminSigupForm

from . import User

class ViewsTest(TestCase):
        
    def test_admin_register_view(self):

        self.user_data = {
            'email': 'admin@example.com',
            'password1': 'admin_password',
            'password2': 'admin_password',
            'first_name': 'Admin',
            'last_name': 'User',
        }

        # Check that no admin user exists with this email before the registration
        self.assertFalse(User.objects.filter(email=self.user_data['email']).exists())

        response = self.client.get(reverse('adminsignup'))
        self.assertIsInstance(response.context['form'], AdminSigupForm)
        response = self.client.post(reverse('adminsignup'), data = self.user_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('adminlogin'))

        # Check if the admin user has been created
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        self.assertTrue(User.objects.filter(email=self.user_data['email']).first().is_superuser)


    def test_auth_login_view(self):
        payload = {
            'email': 'testuser@example.com',
            'password': '_++90test67ty5_password',
        }

        payload2 = {
            'username': 'testuser@example.com',
            'password': '_++90test67ty5_password',
        }


        User.objects.create_user(**payload)
        
        response = self.client.post(reverse('login'), data = payload2)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('afterlogin'))
