from django.urls import path
from . import views

from django.views.generic import TemplateView

from django.urls import path

urlpatterns = [
    path('viewstudent', views.AllStudentsView.as_view(), name='viewstudent'),
    path('booksbystudent', views.StudentBooksView.as_view(), name='viewissuedbookbystudent'),
    
    path('makebookrequest', views.RequestBookView.as_view(), name='makebookrequest'),

]
