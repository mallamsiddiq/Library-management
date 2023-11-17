from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from . import Book, BookIssuance
from student.models import StudentExtra

class BookModelTest(TestCase):
    def test_create_book(self):
        # Create a new book instance
        Book.objects.create(
            name="Test Book",
            isbn=123,
            author="Test Author",
            total_stock=5,
        )

        book = Book.objects.all().first()

        # Verify the attributes of the created book
        self.assertEqual(book.name, "Test Book")
        self.assertEqual(book.isbn, 123)
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.total_stock, 5)

    def test_out_of_shelves(self):
        # Create a book with 0 total copies, no issuances
        book = Book(name="Test Book", isbn=123, author="Test Author", total_stock=0)
        book.save()
        self.assertTrue(book.out_of_shelves())  # No copies available

    def test_available_copies(self):
        # Create a book with 5 total copies and 3 active issuances
        book = Book(name="Test Book", isbn=123, author="Test Author", total_stock=5)
        book.save()
        student1 = StudentExtra.objects.create(email = "test1@m.co", enrollment="12345", branch = "social", first_name="John", last_name="Doe")
        student2 = StudentExtra.objects.create(email = "test2@m.co", enrollment="67890", branch = "tech", first_name="Jane", last_name="Smith")

        # Create 3 active issuances for the book
        book.issuance.create(student=student1)
        book.issuance.create(student=student2)
        book.issuance.create(student=student2)

        self.assertEqual(book.available_copies, 2)  # 3 copies are issued, 2 are available

    def test_str_representation(self):
        # Create a book
        book = Book(name="Test Book", isbn=123, author="Test Author", total_stock=1)
        book.save()
        self.assertEqual(str(book), "Test Book [123]")

class BookIssuanceModelTest(TestCase):
    def setUp(self):
        self.student = StudentExtra.objects.create(
            enrollment="12345",
            first_name="John",
            last_name="Doe",
        )
        self.book = Book.objects.create(
            name="Test Book",
            isbn=123,
            author="Test Author",
            total_stock=1,
        )

    def test_expired_issuance(self):
        issuance = BookIssuance(
            student=self.student,
            book=self.book,
            expirydate=timezone.now().date() - timedelta(days=1),
        )
        issuance.save()
        self.assertTrue(issuance.expired)

    def test_due_in(self):
        expiry_date = timezone.now().date() + timedelta(days=5)
        issuance = BookIssuance(
            student=self.student,
            book=self.book,
            expirydate=expiry_date,
        )
        issuance.save()
        self.assertEqual(issuance.due_in, 5)

    def test_is_qualified(self):
        # Test when book is out of stock

        first_issuance = BookIssuance(student=self.student, book=self.book)
        first_issuance.save()

        issuance = BookIssuance(student=self.student, book=self.book)
        message, is_qualified = issuance.is_qualified()
        self.assertFalse(is_qualified)
        self.assertEqual(message, "Book is not available for issuing.")

        # Test when student has overdue books
        self.book.total_stock += 1
        self.book.save()

        first_issuance.expirydate = timezone.now().date() - timedelta(days=1)
        first_issuance.save()

        issuance = BookIssuance(student=self.student, book=self.book)
        message, is_qualified = issuance.is_qualified()
        self.assertFalse(is_qualified)
        self.assertEqual(message, "Student has overdue books and cannot issue new books.")

        # Test when both book and student are qualified
        self.student.clear_overdue_books()
        issuance = BookIssuance(student=self.student, book=self.book)
        issuance.save()
        message, is_qualified = issuance.is_qualified()
        self.assertTrue(is_qualified)
        self.assertIsNone(message)

    def test_str_representation(self):
        issuance = BookIssuance(
            student=self.student,
            book=self.book,
            expirydate=timezone.now().date() + timedelta(days=7),
        )
        issuance.save()
        expected_str = f"Issued to 12345 | John Doe - Test Book (ISBN: 123)"
        self.assertEqual(str(issuance), expected_str)
