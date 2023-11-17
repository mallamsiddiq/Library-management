from django.test import TestCase
from authapp.forms import AdminSigupForm, StudentSigupForm

class AdminSigupFormTest(TestCase):
    def test_admin_signup_form_valid(self):
        form_data = {
            'email': 'admin@example.com',
            'password1': 'admin_password',
            'password2': 'admin_password',
            'first_name': 'Admin',
            'last_name': 'User',
        }
        form = AdminSigupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_admin_signup_form_invalid(self):
        form_data = {
            'email': 'invalid_email',
            'password1': 'password1',
            'password2': 'password2',
            'first_name': '',
            'last_name': '',
        }
        form = AdminSigupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_admin_signup_form_save(self):
        form_data = {
            'email': 'admin@example.com',
            'password1': 'admin_password',
            'password2': 'admin_password',
            'first_name': 'Admin',
            'last_name': 'User',
        }
        form = AdminSigupForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_student_signup_form_weak_password(self):
        form_data = {
            'email': 'valid_email@mail.co',
            'password1': '1',
            'password2': '1',
            'first_name': 'Smith',
            'last_name': 'John',
            'enrollment': 'random enrollment',
            'branch': 'random branch',
        }
        form = StudentSigupForm(data=form_data)
        self.assertFalse(form.is_valid())
        print(form.errors)
        self.assertIn('This password is too short', form.errors['password2'][0])

        form_data.update({'password1': 'password',
            'password2': 'password',})
        form = StudentSigupForm(data=form_data)
        self.assertIn('This password is too common', form.errors['password2'][0])
        

class StudentSigupFormTest(TestCase):
    def test_student_signup_form_valid(self):
        form_data = {
            'email': 'student@example.com',
            'password1': 'student_password',
            'password2': 'student_password',
            'first_name': 'Student',
            'last_name': 'User',
            'enrollment': '1234567890',
            'branch': 'Computer Science',
        }
        form = StudentSigupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_student_signup_form_invalid(self):
        form_data = {
            'email': 'invalid_email',
            'password1': 'password1',
            'password2': 'password2',
            'first_name': '',
            'last_name': '',
            'enrollment': 'invalid_enrollment',
            'branch': '',
        }
        form = StudentSigupForm(data=form_data)
        self.assertFalse(form.is_valid())
