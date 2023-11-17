import django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from student.models import StudentExtra

User = django.contrib.auth.get_user_model()
     
class AdminSigupForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, 
        help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name','last_name']

    def save(self, commit=True):
        user = super().save(commit=False)  # Get the user instance without saving it yet
        user.is_superuser = True  # Set is_superuser to True
        user.is_staff = True

        if commit:
            user.save()  # Save the user instance
        return user

class StudentSigupForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, 
        help_text="Required. Enter a valid email address.")

    class Meta:
        model = StudentExtra
        fields = ['email', 'password1', 'password2', 'first_name','last_name', 'enrollment', 'branch']