from django.urls import path
from . import views

from django.views.generic import TemplateView

from django.urls import path

urlpatterns = [
    path('', TemplateView.as_view(template_name='base/base.html'), name='home'),
    
    path('adminpanel', views.PanelView.as_view(template_name='library/adminclick.html'), 
                    name='adminpanel'),
    path('studentpanel', views.PanelView.as_view(template_name='library/studentclick.html'), 
                    name='studentpanel'),
    
    path('afterlogin', views.DasboardView.as_view(), name='afterlogin'),

    path('addbook', views.BookCreateView.as_view(), name='addbook'),
    path('viewbooks', views.AllBooksView.as_view(), name='viewbook'),
    # path('viewbook/<int:pk>', views.viewbook_view, name='book-details'),
    path('issuebook', views.IssueBookView.as_view(), name='issuebook'),
    
    path('viewissuedbook', views.AllIssuedBooksView.as_view(), name='viewissuedbook'),
    
    path('aboutus', TemplateView.as_view(template_name='library/aboutus.html'), name='about-us'),
    path('contactus', views.ContactUsView.as_view(), name='contactus'),

    path('pending-requests/', views.PendingBookRequestsView.as_view(), name='admin-pending-requests'),   
    path('pending-requests/accept/<int:pk>/', views.AcceptBookRequestView.as_view(), name='accept_request'),
    path('pending-requests/reject/<int:pk>/', views.RejectBookRequestView.as_view(), name='reject_request'),
]


