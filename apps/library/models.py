from django.db import models
from student.models import StudentExtra
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


class Book(models.Model):
    class Category(models.TextChoices):
        EDUCATION = 'education', 'Education'
        ENTERTAINMENT = 'entertainment', 'Entertainment'
        COMICS = 'comics', 'Comics'
        BIOGRAPHY = 'biography', 'Biography'
        HISTORY = 'history', 'History'
        NOVEL = 'novel', 'Novel'
        FANTASY = 'fantasy', 'Fantasy'
        THRILLER = 'thriller', 'Thriller'
        ROMANCE = 'romance', 'Romance'
        SCIFI = 'scifi', 'Sci-Fi'

    name = models.CharField(max_length = 30)
    isbn = models.PositiveIntegerField()
    author = models.CharField(max_length = 40)
    category = models.CharField(max_length = 30, choices = Category.choices, default = Category.EDUCATION)
    readers = models.ManyToManyField(
        StudentExtra,
        through='BookIssuance',
        related_name = 'books',
    )

    total_stock = models.PositiveIntegerField(default=1)

    @property
    def available_copies(self):
        return self.total_stock - self.issuance.filter(status = 'active').count()
    
    def out_of_shelves(self):
        return self.available_copies <= 0


    def __str__(self):
        return f"{self.name} [{self.isbn}]"


def get_expiry(current = datetime.today()):
    return current + timedelta(days = 15)

class BookIssuance(models.Model):
    
    class Status(models.TextChoices):
        active = 'active', 'active'
        pending = 'pending', 'pending'
        returned = 'returned', 'returned'
        rejected = 'rejected', 'rejected'
    
    status = models.CharField(max_length = 30, choices = Status.choices, default = Status.active)

    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE, related_name="book_issuance")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issuance")
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    @property
    def expired(self):
        return self.due_in < 0
    
    @property
    def due_in(self):
        return (self.expirydate - timezone.now().date()).days

    def is_qualified(self) -> (str, bool):
        if self.book.out_of_shelves():
            return "Book is not available for issuing.", False
        
        # Check if the student has overdue books
        if self.student.has_overdue_books():
            return "Student has overdue books and cannot issue new books.", False

        return None, True 


    def __str__(self):
        return f"Issued to {self.student.enrollment} | {self.student.full_name} - {self.book.name} (ISBN: {self.book.isbn})"

    
    def return_book(self, *args, **kwargs):
        self.status = 'returned'
        super(BookIssuance, self).save(*args, **kwargs)