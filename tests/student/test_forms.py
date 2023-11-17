from django.test import TestCase
from library.models import Book, BookIssuance
from student.forms import RequestBookForm
from datetime import timedelta

from . import StudentExtra

class RequestBookFormTest(TestCase):
    def setUp(self):
        # Create a test student and some test books
        self.login_payload = {
            "email": 'teststudent@example.com',
            "password": "pass12356",

        }

        self.student_payload = {
            "first_name":'Test',
            "last_name":'Student',
            "enrollment":'EN123',
            "branch":'Computer Science',
        }

        self.student = StudentExtra.objects.create_user(**self.login_payload)
        
        for field, value in self.student_payload.items():
            setattr(self.student, field, value)

        self.student.save()
        
        self.book = Book.objects.create(name='Book 1', isbn='123456', author = "author 1", total_stock = 4)

    def test_valid_request(self):
        # Test a valid book issuance request
        form_data = {
            'book': self.book.pk,
            'user': self.student.pk,
            'status': 'active',
        }

        form_data_2 = {
            'book': self.book.pk,
        }

        form = RequestBookForm(data=form_data, curr_student=self.student)
        self.assertTrue(form.is_valid())

        form_2 = RequestBookForm(data=form_data_2, curr_student=self.student)
        self.assertTrue(form_2.is_valid())

        with self.assertRaises(KeyError):
            form_3 = RequestBookForm(data=form_data_2)
            self.assertTrue(form_3.is_valid())

    def test_book_request_out_of_shelves(self):
        # Test a request for a book that is out of shelves
        self.book.total_stock = 0
        self.book.save()
        form_data = {
            'book': self.book.pk,
        }
        form = RequestBookForm(data=form_data, curr_student=self.student)
        self.assertFalse(form.is_valid())
        self.assertIn('Book is not available for issuing.', form.non_field_errors())

    def test_book_request_overdue_books(self):
        # Test a request when the student has overdue books
        # Create a BookIssuance record with an active status and an overdue book
        issuance = BookIssuance.objects.create(student=self.student, book=self.book)
        issuance.expirydate = issuance.issuedate - timedelta(days=1)  # Make it overdue
        issuance.save()

        form_data = {
            'book': self.book.pk,
        }

        form = RequestBookForm(data=form_data, curr_student=self.student)
        self.assertFalse(form.is_valid())
        self.assertIn('Student has overdue books and cannot issue new books.', form.non_field_errors())

    def test_hidden_fields(self):
        # Test that user and status fields are hidden
        form = RequestBookForm(curr_student=self.student)
        self.assertIn('type="hidden"', form.as_p())

    def test_form_labels(self):
        # Test custom labels for book field
        form = RequestBookForm(curr_student=self.student)
        self.assertEqual(form.fields['book'].label, "Books' Names and ISBN")

    def test_empty_book_selection(self):
        # Test that selecting an empty book is not valid
        form_data = {
            'book': '',  # No book selected
            'user': self.student.pk,
            'status': 'active',
        }
        form = RequestBookForm(data=form_data, curr_student=self.student)
        
        self.assertIn('This field is required.', form.errors['book'])
