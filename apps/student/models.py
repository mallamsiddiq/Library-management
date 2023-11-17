from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class StudentExtra(User):
    enrollment = models.CharField(max_length = 40)
    branch = models.CharField(max_length = 40)
    
    #used in issue book
    def __str__(self):
        return f"{self.first_name} [{self.enrollment}]"
    
    
    @property
    def overdue_books(self):
        return self.book_issuance.filter(expirydate__lt=timezone.now(), status = 'active')
    
    def has_overdue_books(self):
        return self.overdue_books.count() > 0

    def clear_overdue_books(self):
        # Get the list of overdue books
        overdue_issuance = self.overdue_books

        # Mark each overdue book as instatus
        for issuance in overdue_issuance:
            issuance.return_book()