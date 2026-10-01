from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from rooms.models import Room


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.room.name} ({self.rating}★)"