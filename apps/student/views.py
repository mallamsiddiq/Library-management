from typing import Any
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import StudentExtra
from .forms import RequestBookForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, ListView, CreateView

from library.models import BookIssuance
from library.views import AdminRequiredMixin

class OnlyStudentInMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return bool(getattr(self.request.user, 'studentextra', False))

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect(reverse_lazy('studentlogin'))

class AllStudentsView(AdminRequiredMixin, ListView):
    model = StudentExtra
    context_object_name = 'students'
    template_name = 'library/viewstudent.html'



class StudentBooksView(OnlyStudentInMixin, ListView):
    model = BookIssuance
    context_object_name = 'book_engagements'
    template_name = 'library/viewissuedbookbystudent.html'

    def get_student(self, _):
        return StudentExtra.objects.get(user_ptr=self.request.user)

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context = super().get_context_data(**kwargs)
        # Fetch active book engagements for the student
        student = self.get_student(context)
        context['student'] = student
        context['book_engagements'] = student.book_issuance.filter(status = 'active')

        context['due_books_engagements'] = student.overdue_books

        # Fetch old (inactive) book engagements for the student
        context['old_books_engagements'] = student.book_issuance.filter(status = 'returned')

        return context
    
    def get_queryset(self):
        # Filter the queryset to include only active issued books and prefetch related books
        return self.model.objects.filter(status = 'active', student = self.request.user)
    

class RequestBookView(OnlyStudentInMixin, CreateView):
    form_class = RequestBookForm
    template_name = 'library/create/requestbook.html'
    success_url = reverse_lazy('makebookrequest')
    model = BookIssuance

    def get_student(self):
        return StudentExtra.objects.get(user_ptr=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['curr_student'] = self.get_student()  # Pass the logged-in user to the form
        return kwargs
    
    def form_valid(self, form):

        form.instance.student = self.get_student()
        form.instance.status = 'pending'

        messages.success(self.request, "Your book request has been submitted successfully.")
        return super().form_valid(form)