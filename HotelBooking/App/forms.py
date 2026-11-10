from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Booking

class CustomSignUpForm(UserCreationForm):
    # Add fields for your UserProfile model with custom widget attributes
    fullname = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Charlotte Hamilton'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'charlotte@example.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        # 1. Let the parent form save the core Django User first
        user = super().save(commit=commit)
        
        if commit:
            # 2. Automatically create and link your UserProfile
            UserProfile.objects.create(
                user=user,
                fullname=self.cleaned_data['fullname'],
                email=self.cleaned_data['email']
            )
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['venue', 'booking_date']
        widgets = {
            'venue': forms.Select(attrs={'class': 'form-input'}),
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        }