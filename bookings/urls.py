from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:room_id>/', views.create_booking, name='create_booking'),
    path('success/<int:pk>/', views.booking_success, name='booking_success'),
    path('my/', views.my_bookings, name='my_bookings'),
]