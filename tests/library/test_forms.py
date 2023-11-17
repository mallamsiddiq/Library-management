from django.test import TestCase
from library.forms import ContactusForm, BookForm, IssuedBookForm
from . import Book
from student.models import StudentExtra
from django import forms
from datetime import timedelta
from django.utils import timezone

class ContactusFormTest(TestCase):
    def test_contactus_form_valid(self):
        data = {
            'Name': 'John Doe',
            'Email': 'john@example.com',
            'Message': 'This is a test message.'
        }
        form = ContactusForm(data=data)
        self.assertTrue(form.is_valid())

    def test_contactus_form_invalid(self):
        data = {
            'Name': '',
            'Email': 'invalid_email',
            'Message': ''
        }
        form = ContactusForm(data=data)
        self.assertFalse(form.is_valid())

class BookFormTest(TestCase):
    def test_book_form_valid(self):
        data = {
            'name': 'Test Book',
            'isbn': 123,
            'author': 'Test Author',
            'category': 'education',
        }
        form = BookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_book_form_invalid(self):
        data = {
            'name': '',
            'isbn': 'invalid_isbn',
            'author': '',
            'category': 'invalid_category',
        }
        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        

class IssuedBookFormTest(TestCase):

    def setUp(self):
        # Create some example data (books and students) for testing
        self.student = StudentExtra.objects.create(
            enrollment="12345",
            first_name="John",
            last_name="Doe",
            email = "test@mail.com"
        )
        self.book = Book.objects.create(
            name="Test Book",
            isbn=123,
            author="Test Author",
            category="education",
        )

    def test_valid_form(self):
        data = {
            'book': self.book,
            'student': self.student,
        }
        form = IssuedBookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_book_not_available(self):
        # Set the book as not available (e.g., out of shelves)
        self.book.total_stock = 0
        self.book.save()

        data = {
            'book': self.book.id,
            'student': self.student.id,
        }
        form = IssuedBookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Book is not available for issuing.', form.non_field_errors())

    def test_student_has_overdue_books(self):
        # Create some overdue books for the student
        
        self.book.total_stock += 1
        self.book.save()
        self.student.book_issuance.create(expirydate=timezone.now().date() - timedelta(days=1), 
                                          book = self.book)

        data = {
            'book': self.book.id,
            'student': self.student.id,
        }
        form = IssuedBookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Student has overdue books and cannot issue new books.', form.non_field_errors())

    def test_empty_form(self):
        # Test with empty form data
        form = IssuedBookForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('book', form.errors)
        self.assertIn('student', form.errors)
