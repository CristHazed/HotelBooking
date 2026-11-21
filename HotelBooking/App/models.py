from decimal import Decimal
import uuid
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime, time
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
    name = models.CharField(max_length=150)                                                     # Name of the Room / Room Number
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES, default='Standard')         # ROOM_TYPES
    capacity = models.IntegerField()                                                            # Capacity (1-4)
    is_available = models.BooleanField(default=True)                                            # Room availability
    price_per_night = models.IntegerField(default=0)                                            # Room Price
    room_description = models.TextField(max_length=5000, default='Failed to load description')  # Room Description

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
        return f"{self.name} (Capacity: {self.capacity}) : [{status}]"

class StandardRoom(Room):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('300.00')
        if not self.pk:
            self.room_type = 'Standard'
            if self.capacity is None:
                self.capacity = 1

    def calculate_StandardRate(self, stay_duration):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if self.guess > self.capacity:
            room_total = (self.guess_count * self.extra_guest_fee) + total_rate
        return room_total
    
class DeluxeRoom(Room):
    class Meta:
        proxy = True
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('75.00')
        if not self.pk:
            self.room_type = 'Deluxe'
            if self.capacity is None:
                self.capacity = 3
        
    def calculate_DeluxeRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate
    
class VIPRoom(Room):
    class Meta:
        proxy = True
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('100.00')
        if not self.pk:
            self.room_type = 'VIP'
            if self.capacity is None:
                self.capacity = 4
        
    def calculate_VIPRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate
    
class DeluxePlusRoom(Room):
    class Meta:
        proxy = True
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('125.00')
        if not self.pk:
            self.room_type = 'Deluxe Plus'
            if self.capacity is None:
                self.capacity = 5
        
    def calculate_DeluxePlusRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate


class Itinerarie(models.Model):
    ITINERARIES_TYPE = [
            ('OUTDOOR & ADVENTURE PACKS', 'Adventure'),
            ('WELLNESS & HYDRO-SPA PACKS', 'Wellness'),
            ('DINING & CULINARY ADD-ONS', 'Dining'),
            ('ENTERTAINMENT & LEISURE PASSES', 'Leisure')
        ]
    Itineraries_type = models.CharField(max_length=50, choices=ITINERARIES_TYPE, default='None')
    itinerary_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    participant_count = models.IntegerField(default=1)
    itinerary_description = models.TextField(max_length=5000)

    def __str__(self):
            return self.itinerary_name

    
    def calculate_rate(self, stay_duration):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        return self.base_rate * stay_duration

class StandardRoom(Room):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('50.00')
        if not self.pk:
            self.room_type = 'Standard'
            if self.capacity is None:
                self.capacity = 2

    def calculate_StandardRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate
    
class DeluxeRoom(Room):
    class Meta:
        proxy = True
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('75.00')
        if not self.pk:
            self.room_type = 'Deluxe'
            if self.capacity is None:
                self.capacity = 3
        
    def calculate_DeluxeRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate
    
class VIPRoom(Room):
    class Meta:
        proxy = True
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('100.00')
        if not self.pk:
            self.room_type = 'VIP'
            if self.capacity is None:
                self.capacity = 4
        
    def calculate_VIPRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate
    
class DeluxePlusRoom(Room):
    class Meta:
        proxy = True
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra_guest_fee = Decimal('125.00')
        if not self.pk:
            self.room_type = 'Deluxe Plus'
            if self.capacity is None:
                self.capacity = 5
        
    def calculate_DeluxePlusRate(self, stay_duration, guest_count):
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        total_rate = self.base_rate * stay_duration
        if guest_count > self.capacity:
            extra_guests = guest_count - self.capacity
            total_rate += extra_guests * self.extra_guest_fee
        return total_rate
# Booking Structure / Booking Handler
class Booking(models.Model):
    reservation_number = models.CharField(max_length=20, unique=True, blank=True)   # Unique Reservations number generated from UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE)                        # Tracks the current active / logged in user
    venue = models.ForeignKey(Room, on_delete=models.CASCADE)                       # Selects the room info the user chose
    booking_date = models.DateTimeField()                                           # The reservation date selected by user
    checkout_date = models.DateTimeField()                                          # Check_out date selected by user
    status = models.CharField(max_length=50, default='Confirmed')                   # Status of the booking
    created_at = models.DateTimeField(auto_now_add=True)                            # Uploads when the booking was created
    itineraries = models.ManyToManyField(Itinerarie,blank=True)
    guess_count = models.IntegerField(default=0)
    extra_guess_fee = models.IntegerField(default=500)

    # Custom save function to save ref number or reservation number
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            unique_code = uuid.uuid4().hex[:8].upper()
            self.reservation_number = f"RES-{unique_code}"

        # saves the booking and checkout date and defaults the time to standard 11pm checkout and 2pm checkin
        if self.booking_date:
            if not isinstance(self.booking_date, datetime):
                self.booking_date = datetime.combine(self.booking_date, time(14, 0, 0))

        if self.checkout_date:
            if not isinstance(self.checkout_date, datetime):
                self.checkout_date = datetime.combine(self.checkout_date, time(11, 0, 0))
        super().save(*args, **kwargs)

    # Function if cancellation is requested
    def cancellation(self):
        self.status = 'Cancelled'
        self.venue.release()        # release() is taken from Room object
        self.save()

    # Calculate total for whole booking
    @property
    def total_cost(self):
        stay_duration = max(
            (self.checkout_date.date() - self.booking_date.date()).days, 0,
        )
        if stay_duration <= 0:
            raise ValueError("Stay duration must be greater than 0")
        room_cost = self.venue.price_per_night * stay_duration
        if self.extra_guess_fee > 0:
            room_total = (self.guess_count * self.extra_guess_fee) + room_cost 
        else:
            room_total = room_cost
        itineraries_total = sum(itinerary.price for itinerary in self.itineraries.all())
        total_booking_cost = room_total + itineraries_total
        return total_booking_cost

    @property
    def current_status(self):
        today = timezone.localdate()

        if self.status.lower() in ['Completed', 'Cancelled']:
            return self.status

        if today > self.checkout_date.date():
            return 'Completed'

        elif self.booking_date.date() == today or (self.booking_date.date() - today).days <= 1:
            return 'Upcoming'

        return self.status

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
