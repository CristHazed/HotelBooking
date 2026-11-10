import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.fullname} ({self.user_id})"

class Room(models.Model):
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

class Booking(models.Model):
    reservation_number = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            unique_code = uuid.uuid4().hex[:8].upper()
            self.reservation_number = f"RES-{unique_code}"
        super().save(*args, **kwargs)

    def cancellation(self):
        self.status = 'Cancelled'
        self.venue.release()
        self.save()

    def __str__(self):
        return f"[{self.reservation_number}] {self.user.username} booked {self.venue.name}"