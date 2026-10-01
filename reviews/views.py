from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rooms.models import Room
from bookings.models import Booking
from .models import Review
from .forms import ReviewForm


@login_required
def submit_review(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    # Must have a confirmed booking
    has_booked = Booking.objects.filter(
        user=request.user, room=room, status='confirmed'
    ).exists()

    if not has_booked:
        messages.error(request, "You can only review rooms you have stayed in.")
        return redirect('rooms:room_detail', pk=room.pk)

    # Already reviewed?
    if Review.objects.filter(user=request.user, room=room).exists():
        messages.info(request, "You have already reviewed this room.")
        return redirect('rooms:room_detail', pk=room.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('rooms:room_detail', pk=room.pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/submit_review.html', {
        'room': room,
        'form': form,
    })