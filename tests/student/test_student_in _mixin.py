from django.test import TestCase
from django.urls import reverse
from . import StudentExtra, User # Import your StudentExtra model

class OnlyStudentInMixinTestCase(TestCase):


    def setUp(self):
        # Create a test user

        self.login_payload = {
            "email": 'teststudent@example.com',
            "password": "pass12356",

        }

        self.student_payload = {
            "first_name":'Test',
            "last_name":'User',
            "enrollment":'EN123',
            "branch":'Computer Science',
        }

        self.student = StudentExtra.objects.create_user(**self.login_payload)
        
        for field, value in self.student_payload.items():
            setattr(self.student, field, value)

        self.student.save()
        
        self.BOOK_REQUEST_URL = reverse('makebookrequest') 

    def test_only_student_in_mixin(self):

        # Make a request to the view with the mixin
        response = self.client.get(self.BOOK_REQUEST_URL)

        # Check whether the user is redirected to the student login page
        self.assertEqual(response.status_code, 302)  # Check for a redirect
        self.assertRedirects(response, reverse('login'))

        # Check whether the user is not redirected if they meet the test_func condition
        self.client.login(**self.login_payload)

        response = self.client.get(self.BOOK_REQUEST_URL)
        self.assertEqual(response.status_code, 200)  # Check for a successful response

        # now log in but not as a student
        self.login_payload.update(email = "newemail@gmail.com")

        User.objects.create_superuser(**self.login_payload)

        response = self.client.get(self.BOOK_REQUEST_URL)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('studentlogin'))