from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from django.contrib import messages 
from . import StudentExtra, User

from django.utils import timezone
from datetime import timedelta

from library.models import BookIssuance, Book

class RequestBookViewTestCase(TestCase):
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

        self.book_instance = Book.objects.create(
            name = "A new book",
            isbn = 12903,
            author = 'new_author',
            category = "scifi",
            total_stock = 3

        )
        
        self.BOOK_REQUEST_URL = reverse('makebookrequest') 

    def get_messages(self, response):
        # Helper function to retrieve messages from the response
        return [m.message for m in messages.get_messages(response.wsgi_request)]
    
        # messages = list(get_messages(response.wsgi_request))

    def test_request_view(self):
        # Log in the user
        
        
        self.client.login(**self.login_payload)

        # Create a test form data
        form_data = {
            'book': self.book_instance.id,
        }
        

        # Get the logged-in user instance
        logged_in_user = get_user(self.client)


        # Submit the request book form
        response = self.client.post(self.BOOK_REQUEST_URL, form_data, follow=True)

        # Check the response status codes
        self.assertEqual(response.status_code, 200)  # Replace with your expected status code

        # Check that the book request was successful
        self.assertTrue(BookIssuance.objects.all().exists())
        
        self.assertTrue(BookIssuance.objects.filter(student=self.student, book=self.book_instance, status= 'pending').exists())
        self.assertIn("Your book request has been submitted successfully.", self.get_messages(response))
        
    def test_request_book_view_book_unavailable(self):
        # Log in the test student
        self.client.login(**self.login_payload)

        logged_in_user = get_user(self.client)
        

        # Set the total_stock of the book to 0, making it unavailable
        self.book_instance.total_stock = 0
        self.book_instance.save()

        # Make a GET request to the view
        response = self.client.get(self.BOOK_REQUEST_URL)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Create a BookIssuance form data
        form_data = {
            'book': self.book_instance.id,
        }

        # Make a POST request to the view with the form data
        response = self.client.post(self.BOOK_REQUEST_URL, data=form_data, follow=True)

        # Check that the response status code is 200 (OK) after the form submission
        self.assertEqual(response.status_code, 200)

        # Check that an error message is displayed in the response content
        
        self.assertFalse(BookIssuance.objects.filter(student=self.student, book=self.book_instance, status= 'pending').exists())
        form = response.context['form']
        self.assertIn("Book is not available for issuing.", form.non_field_errors())
        

    def test_request_book_view_overdue_books(self):
        # Log in the test student
        self.client.login(**self.login_payload)

        # Create a BookIssuance record with an active status and an overdue book
        issuance = BookIssuance.objects.create(student=self.student, book=self.book_instance)
        issuance.expirydate = issuance.issuedate - timedelta(days=1)  # Make it overdue
        issuance.save()

        # Create a BookIssuance form data
        form_data = {
            'book': self.book_instance.id,  # Replace with the actual book ID
        }

        # Make a POST request to the view with the form data
        response = self.client.post(self.BOOK_REQUEST_URL, data=form_data, follow=True)

        # Check that the response status code is 200 (OK) after the form submission
        self.assertEqual(response.status_code, 200)

        # Check that an error message is displayed in the form content
        self.assertFalse(BookIssuance.objects.filter(student=self.student, book=self.book_instance, status= 'pending').exists())
        
        form = response.context['form']
        
        self.assertIn("Student has overdue books and cannot issue new books.", form.non_field_errors())


    def test_request_book_view_un_auth(self):

        # Make a GET request to the view
        response = self.client.get(self.BOOK_REQUEST_URL)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.BOOK_REQUEST_URL}")

        # now log in but not as a student
        self.login_payload.update(email = "newemail@gmail.com")

        User.objects.create_superuser(**self.login_payload)

        self.client.login(**self.login_payload)

        response = self.client.get(self.BOOK_REQUEST_URL)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('studentlogin'))