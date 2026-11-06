from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def landing_page(request):
    return render(request, 'pages/landing.html')

def login_signup_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Incorrect email of password. Please try again!')
            return redirect('login_signup')

@login_required(login_url='pages/login_singup/')
def homepage(request):
    user_profile = request.user.userprofile
    context = {'profile': user_profile}
    return render(request, 'pages/home.html', context)