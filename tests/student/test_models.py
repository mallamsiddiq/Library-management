from django.test import TestCase
from django.utils import timezone
from . import StudentExtra, User
from library.models import Book

class StudentExtraModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.student = StudentExtra(
            email='teststudent@example.com',
            first_name='Test',
            last_name='User',
            password = "pass12356",
            enrollment='EN123',
            branch='Computer Science',
        )

        self.student.save()

        self.book_instance = Book.objects.create(
            name = "A new book",
            isbn = 12903,
            author = 'new_author',
            category = "scifi",
            total_stock = 3

        )

    def test_str_method(self):
        self.assertEqual(str(self.student), 'Test [EN123]')

    def test_overdue_books_property(self):

        # Create test BookIssuance instances for the student
        self.student.book_issuance.create(
            book=self.book_instance,  # Replace with a valid book instance
            
            expirydate=timezone.now() - timezone.timedelta(days=1),  # Expired book
            status='active',  # Active book
        )

        self.student.book_issuance.create(
            book=self.book_instance,  # Replace with a valid book instance
            
            expirydate=timezone.now() + timezone.timedelta(days=1),  # Valid book
            status='active',  # Active book
        )

        # Test the overdue_books property
        overdue_books = self.student.overdue_books
        self.assertEqual(overdue_books.count(), 1)  # Expecting 1 overdue book

        # Test the has_overdue_books method
        has_overdue = self.student.has_overdue_books()
        self.assertTrue(has_overdue)  # Expecting True

    def test_clear_overdue_books_method(self):
    
        # Create a test BookIssuance instance for the student
        issuance = self.student.book_issuance.create(
            book=self.book_instance,  # Replace with a valid book instance
            
            expirydate=timezone.now() - timezone.timedelta(days=1),  # Expired book
            status='active',  # Active book
        )

        # Confirm has due books
        self.assertTrue(self.student.has_overdue_books())
        
        # Call the clear_overdue_books method
        self.student.clear_overdue_books()

        # Check if the book is no longer active
        issuance.refresh_from_db()
        
        self.assertFalse(self.student.has_overdue_books())
        self.assertFalse(issuance.status == 'active')  # Expecting False

    def test_create_student_from_user(self):

        user = User.objects.create(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password = "pass12356",
        )

        student = StudentExtra(
            user_ptr = user,
            enrollment='EN123',
            branch='Computer Science',
        )

        student.save()

        print(User.objects.all())
        print(StudentExtra.objects.all())

        # Confirm has due books
        # self.assertTrue(self.student.has_overdue_books())
        
        # # Call the clear_overdue_books method
        # self.student.clear_overdue_books()

        # # Check if the book is no longer active
        # issuance.refresh_from_db()
        
        # self.assertFalse(self.student.has_overdue_books())
        # self.assertFalse(issuance.status == 'active')  # Expecting False

