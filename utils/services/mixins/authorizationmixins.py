
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('studentlogin'))
        return redirect(reverse_lazy('adminlogin'))
    




class OnlyStudentInMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return bool(getattr(self.request.user, 'studentextra', False))

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect(reverse_lazy('studentlogin'))

