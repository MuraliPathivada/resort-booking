from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rooms.models import Room
from .models import Booking
from .forms import BookingForm


@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guests = form.cleaned_data['guests']

            nights = (check_out - check_in).days
            total_price = room.price_per_night * nights

            booking = Booking.objects.create(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                guests=guests,
                total_price=total_price,
                status='pending',
            )
            messages.success(request, f"Booking created! ID: #{booking.id}")
            return redirect('bookings:booking_success', pk=booking.pk)
    else:
        form = BookingForm(room=room)

    return render(request, 'bookings/create_booking.html', {
        'room': room,
        'form': form,
    })


@login_required
def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})