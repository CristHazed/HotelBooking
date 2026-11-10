from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomSignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookingForm
from django.db import IntegrityError

from django.contrib.admin.views.decorators import staff_member_required
from .models import UserProfile, Room, Booking
from django.db.models import Count

# Create your views here.

# Landing Page Template
def landing_page(request):
    available_rooms = Room.objects.filter(is_available=True)
    room_groups = []

    for room_type, label in Room.ROOM_TYPES:
        count = available_rooms.filter(room_type=room_type).count()
        if count:
            room_groups.append({
                "value": room_type,
                "label": label,
                "count": count,
            })

    booking_form = BookingForm()
    booking_form.fields["venue"].queryset = (
        available_rooms.order_by("room_type", "name")
    )

    return render(request, "page/landing.html", {
        "booking_form": booking_form,
        "room_groups": room_groups,
    })


# Sign Up Template
def signup_view(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)

        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.add_error(
                    None,
                    "We couldn't create your account. Please check your details and try again.",
                )
            else:
                messages.success(
                    request,
                    "Your account was created successfully. Please sign in.",
                )
                return redirect("login")
    else:
        form = CustomSignUpForm()

    return render(request, "page/signup.html", {"form": form})

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
def homepage(request):
    profile = UserProfile.objects.filter(user=request.user).first()

    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("venue")
        .order_by("-created_at")
    )

    type_counts = (
        Room.objects
        .filter(is_available=True)
        .values("room_type")
        .annotate(count=Count("id"))
        .order_by("room_type")
    )
    type_labels = dict(Room.ROOM_TYPES)

    room_type_summary = [
        {
            "label": type_labels.get(row["room_type"], row["room_type"]),
            "count": row["count"],
        }
        for row in type_counts
    ]

    context = {
        "profile": profile,
        "recent_bookings": bookings[:5],
        "booking_count": bookings.count(),
        "available_room_count": Room.objects.filter(is_available=True).count(),
        "room_type_summary": room_type_summary,
    }
    return render(request, "page/home.html", context)

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

# Renders successfull booking information
@login_required
def booking_success_view(request):
    return render(request, 'page/booking_success.html')

# Renders receipt or confirmation and the ref number
@login_required
def receipt(request, reservation_number):
    booking = get_object_or_404(
        Booking.objects.select_related("venue"),
        reservation_number=reservation_number,
        user=request.user,
    )
    return render(request, "page/confirmation.html", {"booking": booking})

# helps Route staff to manual booking for walk in customers
def manual_book(request):
    return render(request, 'page/manual_book.html')

# Admin dashboard login
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

# Function to change room status : Overrides status if issues occur
@staff_member_required
def toggle_room_status(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.is_available = not room.is_available
    room.save()
    return redirect('custom_admin')

# Reference number search 
@staff_member_required
def verify_reservation_view(request):
    booking = None
    query = request.GET.get('q')
    if query:
        # Search by reservation code or username
        booking = Booking.objects.filter(reservation_number__iexact=query).first()
    
    return render(request, 'page/verify_reservation.html', {'booking': booking, 'query': query})