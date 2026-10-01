import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from .models import Payment


@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if booking.status == 'confirmed':
        messages.info(request, "This booking is already confirmed.")
        return redirect('bookings:booking_success', pk=booking.pk)

    return render(request, 'payments/payment_page.html', {'booking': booking})


@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if request.method == 'POST':
        method = request.POST.get('method', 'upi')

        # Fake transaction ID
        transaction_id = f"MOCK-{uuid.uuid4().hex[:10].upper()}"

        Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            method=method,
            status='success',
            transaction_id=transaction_id,
        )

        booking.status = 'confirmed'
        booking.save()

        messages.success(request, "Payment successful!")
        return redirect('payments:payment_success', booking_id=booking.pk)

    return redirect('payments:payment_page', booking_id=booking.pk)


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    payment = booking.payments.filter(status='success').first()
    return render(request, 'payments/payment_success.html', {
        'booking': booking,
        'payment': payment,
    })