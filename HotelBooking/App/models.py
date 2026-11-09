from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.fullname} ({self.user_id})"

class Venue(models.Model):
    name = models.CharField(max_length=150)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def book(self):
        if self.is_available:
            self.is_available = False
            self.save()
            return True
        return False

    def release(self):
        self.is_available = True
        self.save()

    def __str__(self):
        status = "Available" if self.is_available else "Booked"
        return f"{self.name} (Capacity: {self.capacity}) - [{status}]"

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