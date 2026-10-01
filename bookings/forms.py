from django import forms
from datetime import date
from rooms.models import Room
from .models import Booking


class BookingForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    guests = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room

    def clean_check_in(self):
        check_in = self.cleaned_data['check_in']
        if check_in < date.today():
            raise forms.ValidationError("Check-in date cannot be in the past.")
        return check_in

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        guests = cleaned.get('guests')

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError("Check-out must be after check-in.")

            if self.room and not Booking.is_room_available(self.room, check_in, check_out):
                raise forms.ValidationError("Sorry, this room is not available for those dates.")

        if guests and self.room and guests > self.room.capacity:
            raise forms.ValidationError(f"Max capacity is {self.room.capacity} guests.")

        return cleaned