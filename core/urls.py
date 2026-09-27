from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('outfit/<int:pk>/', views.outfit_detail, name='outfit_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('manage-bookings/<int:pk>/update/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
