from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomSignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

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
