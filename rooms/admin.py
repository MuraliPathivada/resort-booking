from django.contrib import admin
from .models import Room, RoomImage, Amenity


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'price_per_night', 'capacity', 'is_active')
    list_filter = ('room_type', 'is_active')
    search_fields = ('name',)
    inlines = [RoomImageInline]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')