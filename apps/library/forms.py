from django import forms
from django.contrib.auth import get_user_model
from student.models import StudentExtra
from .models import Book, BookIssuance

User = get_user_model()


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,
                              widget=forms.Textarea(attrs={'rows': 3, 
                                                           'cols': 30, 
                                                           'is_textarea': True}))


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields=['name', 'isbn', 'author', 'category']


class IssuedBookForm(forms.ModelForm):

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label="Books' Names and ISBN",
        label="Books' Names and ISBN",
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    student = forms.ModelChoiceField(
        queryset=StudentExtra.objects.all(),
        empty_label="Students' Names and Enrollment",
        label="Students' Names and Enrollment",
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the display values for the choices
        self.fields['book'].label_from_instance = lambda obj: f"{obj.name} [{obj.isbn}]"
        self.fields['student'].label_from_instance = lambda obj: f"{obj.full_name} [{obj.enrollment}]"

    def is_qualified(self):
        student = self.cleaned_data['student']
        book = self.cleaned_data['book']

        if book.out_of_shelves():
            raise forms.ValidationError("Book is not available for issuing.")

        if student.has_overdue_books():
            raise forms.ValidationError("Student has overdue books and cannot issue new books.")
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.is_valid():
            self.is_qualified()
        
        return cleaned_data

    
    class Meta:
        model = BookIssuance
        fields = ('student', 'book')
