from django.urls import path
from . import views

urlpatters = [
    path('', views.landing_page, name='landing'),
    path('login_singup/', views.login_signup_page, name='login_signup'),
    path('home/', views.homepage, name='homepage')
]