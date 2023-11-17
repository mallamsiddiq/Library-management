from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView



urlpatterns = [

    path('login/', views.AuthLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('adminsignup', views.AdminRegisterView.as_view(), name='adminsignup'),
    path('studentsignup', views.StudentRegisterView.as_view(), name='studentsignup'),

    path('adminlogin', LoginView.as_view(template_name='authapp/adminlogin.html'), name='adminlogin'),
    path('studentlogin', LoginView.as_view(template_name='authapp/studentlogin.html'), name='studentlogin'),

    # Add more authentication-related URLs as needed
]


