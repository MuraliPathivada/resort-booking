from django.db import models

class Amenity(models.Model):
    name =models.CharField(max_length=50)
    icon = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('deluxe', 'Deluxe'),
        ('suite','Suite'),
    ]
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=50,choices=ROOM_TYPES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2)
    total_rooms = models.PositiveIntegerField(default=1)
    amenities = models.ManyToManyField(Amenity,blank=True)
    is_active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.room_type})"

class RoomImage(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='rooms/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"image for {self.room.name}"