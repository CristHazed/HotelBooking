from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Booking, UserProfile, Itinerarie, RoomImage

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_available')
    search_fields = ('name',)
    inlines = [RoomImageInline]

admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(Itinerarie)