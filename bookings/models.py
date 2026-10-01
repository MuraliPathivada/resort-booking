from django.db import models
from django.conf import settings
from rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_room_available(room, check_in, check_out):
        """
        Returns True if at least one unit of the room is free for the given range.
        """
        overlapping_count = Booking.objects.filter(
            room=room,
            status='confirmed',
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).count()
        return overlapping_count < room.total_rooms
    
    def __str__(self):
        return f"Booking #{self.id} - {self.room.name} - {self.user.username}"