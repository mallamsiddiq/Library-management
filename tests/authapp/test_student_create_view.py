from django.test import TestCase
from authapp.forms import StudentSigupForm
from student.models import StudentExtra
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentRegisterViewTest(TestCase):
    def test_view_redirects_to_success_url(self):
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

        response = self.client.post(reverse('studentsignup'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('studentlogin'))

    def test_view_invalid_form_data(self):
        form_data = {
            'email': 'invalid_email',
            'password1': 'password1',
            'password2': 'password2',
            'first_name': '',
            'last_name': '',
            'enrollment': 'invalid_enrollment',
            'branch': '',
        }
        response = self.client.post(reverse('studentsignup'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Expecting a form re-render

        # Ensure the form errors are present in the response
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        # Add more form error checks for other fields

    def test_view_duplicate_email(self):
        # Create a user with the same email address before registration
        StudentExtra.objects.create(
            email='student@example.com',
            password='existing_password',
            first_name='Existing',
            last_name='User',
            enrollment='1234567890',
            branch='Computer Science',
        )

        form_data = {
            'email': 'student@example.com',
            'password1': 'student_password',
            'password2': 'student_password',
            'first_name': 'Student',
            'last_name': 'User',
            'enrollment': '1234567890',
            'branch': 'Computer Science',
        }
        response = self.client.post(reverse('studentsignup'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Expecting a form re-render

        # Ensure the form error for duplicate email is present in the response
        self.assertFormError(response, 'form', 'email', 'User with this Email already exists.')

    def test_view_redirect_with_next_param(self):
        form_data = {
            'email': 'student@example.com',
            'password1': 'student_password',
            'password2': 'student_password',
            'first_name': 'Student',
            'last_name': 'User',
            'enrollment': '1234567890',
            'branch': 'Computer Science',
        }
        next_url = reverse('studentlogin')  # A custom redirect URL
        response = self.client.post(f'{reverse("studentsignup")}?next={next_url}', data=form_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, next_url)

    # Add more test cases to cover other edge cases if necessary
