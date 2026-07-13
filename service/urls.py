from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('gallery/', views.gallery, name='gallery'),
    path('logout/', views.logout_view, name='logout'),
    path('provider_register/', views.provider_register, name='provider_register'),
    path("provider/dashboard/",views.provider_dashboard,name="provider_dashboard"),
    path("booking/<int:booking_id>/accept/",views.accept_booking,name="accept_booking"),
    path("booking/<int:booking_id>/reject/",views.reject_booking,name="reject_booking"),
    path("booking/<int:booking_id>/complete/",views.complete_booking,name="complete_booking"),
    path("customer/dashboard/",views.customer_dashboard,name="customer_dashboard"),
    path('provider/<slug:slug>/', views.provider_detail, name='provider_detail'),
    path("provider/<slug:slug>/book/",views.book_service,name="book_service"),
]