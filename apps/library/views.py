from typing import Any
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import BookForm, ContactusForm, IssuedBookForm
from .models import Book, BookIssuance
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView
from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone

def is_admin(user):
    return user.is_superuser

class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('studentlogin'))
        return redirect(reverse_lazy('adminlogin'))

class DasboardView(LoginRequiredMixin, TemplateView):

    def get_template_names(self) -> list[str]:
        if self.request.user.is_superuser:
            return ('library/adminafterlogin.html',)
        return ('library/studentafterlogin.html')


class PanelView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
        return super().get(request, *args, **kwargs)

class BookCreateView(AdminRequiredMixin, CreateView):
    form_class = BookForm
    template_name = 'library/create/addbook.html'
    success_url = reverse_lazy('book-details')

    def get_success_url(self):
        redirect_url = self.request.GET.get('next', self.success_url)
        return redirect_url

    def form_valid(self, form):
        _ = form.save()
        return render(self.request, 'library/success/bookadded.html')

class AllBooksView(AdminRequiredMixin, ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'library/viewbook.html'


class IssueBookView(AdminRequiredMixin, CreateView):
    form_class = IssuedBookForm
    template_name = 'library/create/issuebook.html'
    success_url = reverse_lazy('book-details')
    model = BookIssuance

    def get_success_url(self):
        redirect_url = self.request.GET.get('next', self.success_url)
        return redirect_url
    
    def form_valid(self, form):
        form.save()
        return render(self.request, 'library/success/bookissued.html')

    
class AllIssuedBooksView(AdminRequiredMixin, ListView):
    model = BookIssuance
    context_object_name = 'issuedbooks'
    template_name = 'library/viewissuedbook.html'
    
    def get_queryset(self):
        # Filter the queryset to include only active issued books and prefetch related books
        return self.model.objects.filter(status = 'active')
    

class PendingBookRequestsView(AdminRequiredMixin, ListView):
    model = BookIssuance
    template_name = 'library/pending_requests.html'  # Create the template for the admin view
    context_object_name = 'pending_requests'  # Name to use in the template for the list of pending requests

    def get_queryset(self):
        # Retrieve pending book requests
        return BookIssuance.objects.filter(expirydate__gt=timezone.now(), status = 'pending')

    # Add any additional context data if needed



class AcceptBookRequestView(DetailView):
    model = BookIssuance
    template_name = 'library/pending_requests.html'  # Create a template for the accept request view

    def get(self, request, *args, **kwargs):
        book_request = self.get_object()
        book_request.status = 'active'

        err_msg, is_qualified = book_request.is_qualified()
        if is_qualified:
            book_request.save()
            messages.success(self.request, "Book request successfully Accepted")
        else:
            messages.error(self.request, err_msg)
        return redirect(reverse_lazy('admin-pending-requests'))


class RejectBookRequestView(DetailView):
    model = BookIssuance
    template_name = 'library/pending_requests.html'  # Create a template for the reject request view

    def get(self, request, *args, **kwargs):
        book_request = self.get_object()
        book_request.status = 'rejected'
        book_request.save()

        messages.success(self.request, "Book request successfully Rejected")
        return redirect('admin-pending-requests')


class ContactUsView(FormView):
    form_class = ContactusForm
    template_name = 'library/create/contactus.html'
    success_template_name = 'library/success/contactussuccess.html'

    def form_valid(self, form):
        email = form.cleaned_data['Email']
        name = form.cleaned_data['Name']
        message = form.cleaned_data['Message']

        # Send the email
        send_mail(f'{name} || {email}', message, settings.EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently=False)
        
        return render(self.request, self.success_template_name)
    

    