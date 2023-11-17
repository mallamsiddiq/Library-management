from django.test import TestCase
from django.contrib.auth import get_user_model
from authapp.models import User
authUser = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.admin_user_data = {
            'email': 'testuser@example.com',
            "password":"testpassword"
        }

        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'balance': 100.0,
        }
        
        self.user_data.update(self.admin_user_data)

    def test_auth_user(self):

        self.assertEqual(User, authUser)


    def test_create_user(self):
        user = User.objects.create(**self.user_data)

        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.balance, self.user_data['balance'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(**self.admin_user_data)

        self.assertEqual(admin_user.email, self.user_data['email'])
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)

    def test_str_method(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])
