import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Users Information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.fullname} ({self.user_id})"

# Room Models
class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard Room'),
        ('Deluxe', 'Deluxe / Suite'),
        ('VIP', 'Important Guess'),
        ('Deluxe Plus', 'Delux Capacity')
    ]
    name = models.CharField(max_length=150)                                             # Name of the Room / Room Number
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES, default='Standard') # ROOM_TYPES
    capacity = models.IntegerField()                                                    # Capacity (1-4)
    is_available = models.BooleanField(default=True)                                    #  Room availability

    # Books the rooms
    def book(self):
        if self.is_available:
            self.is_available = False
            self.save()
            return True
        return False

    # Cancellation room status update
    def release(self):
        self.is_available = True
        self.save()

    def __str__(self):
        status = "Available" if self.is_available else "Booked"
        return f"{self.name} (Capacity: {self.capacity}) - [{status}]"

# Booking Structure / Booking Handler
class Booking(models.Model):
    reservation_number = models.CharField(max_length=20, unique=True, blank=True)   # Unique Reservations number generated from UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE)                        # Tracks the current active / logged in user
    venue = models.ForeignKey(Room, on_delete=models.CASCADE)                       # Selects the room info the user chose
    booking_date = models.DateTimeField()                                           # The reservation date selected by user
    status = models.CharField(max_length=50, default='Confirmed')                   # Status of the booking
    created_at = models.DateTimeField(auto_now_add=True)                            # Uploads when the booking was created

    # Custom save function to save ref number or reservation number
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            unique_code = uuid.uuid4().hex[:8].upper()
            self.reservation_number = f"RES-{unique_code}"
        super().save(*args, **kwargs)

    # Function if cancellation is requested
    def cancellation(self):
        self.status = 'Cancelled'
        self.venue.release()        # release() is taken from Room object
        self.save()

    def __str__(self):
        return f"[{self.reservation_number}] {self.user.username} booked {self.venue.name}"
      
      
# EXCEPTIONS
class InvalidRoomSelectionError(Exception):
    pass

class InvalidStayDurationError(Exception):
    pass

class OccupiedRoomBookingError(Exception):
    pass

# GUEST MODEL
class Guest:
    def __init__(self, name):
        if not name or not name.strip():
            raise ValueError("Guest name cannot be empty.")
        self.name = name.strip()
