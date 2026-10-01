from rooms.models import Room


def home(request):
    featured_rooms = Room.objects.filter(is_active=True)[:3]
    return render(request, 'core/home.html', {
        'featured_rooms': featured_rooms
    })

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            messages.success(request, "Thanks! We'll get back to you soon.")
            return redirect('core:contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

def about_view(request):
    return render(request, 'core/about.html')

from rooms.models import RoomImage


def gallery_view(request):
    images = RoomImage.objects.select_related('room').all()
    return render(request, 'core/gallery.html', {'images': images})