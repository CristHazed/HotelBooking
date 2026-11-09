from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.CharField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    user_id = models.IntegerField()

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


    