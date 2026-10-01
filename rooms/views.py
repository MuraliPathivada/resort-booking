from django.shortcuts import render, get_object_or_404
from .models import Room


def room_list(request):
    rooms = Room.objects.filter(is_active=True)
    return render(request, 'rooms/room_list.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk, is_active=True)
    reviews = room.reviews.all()

    avg_rating = 0
    if reviews.exists():
        avg_rating = round(sum(r.rating for r in reviews) / reviews.count(), 1)

    can_review = False
    if request.user.is_authenticated:
        from bookings.models import Booking
        from reviews.models import Review
        has_booked = Booking.objects.filter(
            user=request.user, room=room, status='confirmed'
        ).exists()
        already_reviewed = Review.objects.filter(user=request.user, room=room).exists()
        can_review = has_booked and not already_reviewed

    return render(request, 'rooms/room_detail.html', {
        'room': room,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'can_review': can_review,
    })