# projectname/urls.py
from django.contrib import admin
from django.urls import include, path
from django.urls import reverse_lazy

from django.shortcuts import redirect

# def custom_404_view(*args):
#     return redirect(reverse_lazy('home'))

# handler404 = 'core.urls.custom_404_view'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls'), name='auth'),
    path('', include('library.urls')),
    path('student/', include('student.urls')),
    path('auth/', include('authapp.urls')),  # Include authentication app URLs
]
