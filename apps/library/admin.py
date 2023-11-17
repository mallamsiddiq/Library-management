from django.contrib import admin
from .models import Book, BookIssuance

admin.site.register(Book)

admin.site.register(BookIssuance)

# Register your models here.
