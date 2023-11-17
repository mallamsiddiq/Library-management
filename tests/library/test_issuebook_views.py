from django.test import TestCase
from django.urls import reverse
from student.models import StudentExtra
from . import Book, BookIssuance
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()

class IssueBookViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email = "admin123@g.co",
            password = "admin1234",
        )

        self.student = StudentExtra.objects.create(
            email = 'student@example.com',
            password = 'student_password',
            first_name = 'Student',
            last_name = 'User',
            enrollment = '1234567890',
            branch = 'Computer Science',)
        
        self.book = Book.objects.create(
            name="Test Book",
            isbn=123,
            author="Test Author",
            category="education",
        )

    def test_issue_book_with_valid_data(self):
        # Log in the admin user
        self.client.login(email = "admin123@g.co", password = "admin1234",)

        data = {
            'student': self.student.pk,
            'book': self.book.pk,
        }
        response = self.client.post(reverse('issuebook'), data)

        # Verify that the book issuance record is created
        self.assertEqual(BookIssuance.objects.count(), 1)

        # Check if the form submission is successful and the response contains the bookissued.html template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/success/bookissued.html')

        

    def test_issue_book_with_invalid_data(self):
        # Log in the admin user
        self.client.login(email = "admin123@g.co", password = "admin1234",)

        # Set up the student with overdue books
        self.book.total_stock += 1
        self.book.save()
        self.student.book_issuance.create(expirydate=timezone.now().date() - timedelta(days=1), 
                                          book = self.book)

        self.student.save()

        data = {
            'student': self.student.pk,
            'book': self.book.pk,
        }
        response = self.client.post(reverse('issuebook'), data)

        # Check if the form submission is not successful and the response remains on the issuebook.html template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/create/issuebook.html')

        # Verify that the form contains validation errors for the 'student' field
        form = response.context['form']
        self.assertIn("Student has overdue books and cannot issue new books.", form.non_field_errors())

        # Reset the student's overdue books status
        self.student.has_overdue_books = False
        self.student.save()

    def test_issue_book_without_login(self):
        data = {
            'student': self.student.pk,
            'book': self.book.pk,
        }
        response = self.client.post(reverse('issuebook'), data)

        # Check if the response is a redirect to the login page
        self.assertEqual(response.status_code, 302)  # 302 is a redirect status code
        self.assertRedirects(response, reverse('studentlogin'))

        # Verify that the book issuance record is not created
        self.assertEqual(BookIssuance.objects.count(), 0)
