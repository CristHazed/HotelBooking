from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomSignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookingForm

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Room, Booking

# Create your views here.

# Landing Page Template
def landing_page(request):
    return render(request, 'page/landing.html')


# Sign Up Template
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignUpForm()

    return render(request, 'page/signup.html', {'form': form})

# Login Page Template
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage') 
    else:
        form = AuthenticationForm()

    return render(request, 'page/login.html', {'form': form})

# Log In required Templates
@login_required
# Home Page Template
def homepage(request):
    return render(request, 'page/home.html')

@login_required
def create_booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            venue = booking.venue

            if venue.book():
                booking.user = request.user
                booking.status = "Confirmed"
                booking.save()
                
                return render(request, 'page/booking_success.html', {'booking': booking})
            else:
                form.add_error('venue', 'Sorry, this room/venue is already booked.')
    else:
        form = BookingForm()

    return render(request, 'page/form.html', {'form': form})

def booking_success_view(request):
    return render(request, 'page/booking_success.html')

def receipt(request):
    return render(request, 'page/confirmation.html')


@staff_member_required
def custom_admin_dashboard(request):
    profiles = UserProfile.objects.all()
    rooms = Room.objects.all()
    bookings = Booking.objects.all()

    context = {
        'profiles': profiles,
        'rooms': rooms,
        'bookings': bookings,
    }
    return render(request, 'page/admin_dashboard.html', context)

# Optional: View to toggle or modify room availability directly
@staff_member_required
def toggle_room_status(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.is_available = not room.is_available
    room.save()
    return redirect('custom_admin')

@staff_member_required
def verify_reservation_view(request):
    booking = None
    query = request.GET.get('q')
    if query:
        # Search by reservation code or username
        booking = Booking.objects.filter(reservation_number__iexact=query).first()
    
    return render(request, 'page/verify_reservation.html', {'booking': booking, 'query': query})