from django import forms
from django.forms import HiddenInput
from library.models import Book, BookIssuance

class RequestBookForm(forms.ModelForm):

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        empty_label="Select a book to request",
        label="Books' Names and ISBN",
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    user = forms.CharField(widget=HiddenInput(), required=False)  # Hidden user field
    status = forms.CharField(widget=HiddenInput(), required=False)  # Hidden status field

    def __init__(self, *args, **kwargs):
        self.curr_student = kwargs.pop('curr_student')
        super().__init__(*args, **kwargs)
        self.fields['book'].label_from_instance = lambda obj: f"{obj.name} [{obj.isbn}]"

    def clean(self):
        cleaned_data = super().clean()

        if self.is_valid():
            book = cleaned_data.get('book')
            print("=======      >>>> \n ."*3, cleaned_data.get('user'))
            student = self.curr_student

            message, is_qualified = self._meta.model(student=student, book=book).is_qualified()

            if not is_qualified:
                raise forms.ValidationError(message)

        return cleaned_data

    class Meta:
        model = BookIssuance
        fields = ('book', 'user', 'status')
