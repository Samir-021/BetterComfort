from tempfile import template
from tkinter.font import names
from django.urls import path, include, register_converter
from django.contrib.auth import views as auth_views
from . import views,converters
from .custom_filters import register

register_converter(converters.FloatConverter, 'float')

urlpatterns = [
 path('', views.home,name='home'),
 path('login/', auth_views.LoginView.as_view(template_name='hotels/login.html'), name='login'),
 path('logout/', views.custom_logout, name='logout'),
 path('admin/login/', auth_views.LoginView.as_view(), name='admin_login'),
 path('admin/logout/', auth_views.LogoutView.as_view(), name='admin_logout'),
 path('register/', views.register, name='register'),
 path('about/', views.about,name='about'),
 path('search/', views.search_hotels, name='search_hotels'),
 path('details/<str:lat>/<str:lon>/<str:name>/', views.hotel_details, name='hotel_details'),
 path("favorites", views.favorites_list, name="favorites_list"),
 path("save-favorite/", views.save_favorite, name="save_favorite"),
 path("delete-favorite/<int:favorite_id>/", views.delete_favorite, name="delete_favorite"),
 path('hotel/<float:lat>/<float:lon>/<str:name>/', views.hotel_details, name='hotel_details'),
 path('services/', views.services,name='services'),
 path("error/", views.error_page, name="error_page"),
 path('book/<str:hotel_name>/<float:lat>/<float:lon>/', views.book_hotel, name='book_hotel'),
 path('booking-success/', views.booking_success, name='booking_success'),
 path('my-bookings/', views.my_bookings, name='my_bookings'),
 path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]