import django
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.contrib.auth.views import LogoutView, LoginView

from . import forms 


User = django.contrib.auth.get_user_model()


class AdminRegisterView(CreateView):
    form_class = forms.AdminSigupForm
    template_name = 'authapp/adminsignup.html'
    success_url = reverse_lazy('adminlogin')

    def get_success_url(self):
        redirect_url = self.request.GET.get('next', self.success_url)
        return redirect_url
    
class StudentRegisterView(CreateView):
    form_class = forms.StudentSigupForm
    template_name = 'authapp/studentsignup.html'
    success_url = reverse_lazy('studentlogin')

    def get_success_url(self):
        redirect_url = self.request.GET.get('next', self.success_url)
        return redirect_url

class AuthLoginView(LoginView):
    template_name = 'authapp/studentlogin.html'
    success_url = reverse_lazy('afterlogin')  

class LogoutView(LogoutView):
    template_name = 'authapp/index.html'