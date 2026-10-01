from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('process/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
]