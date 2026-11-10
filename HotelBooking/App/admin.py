from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Booking, UserProfile

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_available')
    search_fields = ('name',)

admin.site.register(Booking)
admin.site.register(UserProfile)