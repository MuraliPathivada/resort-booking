from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'guests', 'total_price', 'status')
    list_filter = ('status', 'check_in')
    search_fields = ('user__username', 'room__name')