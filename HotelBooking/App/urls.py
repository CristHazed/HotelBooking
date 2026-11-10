from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view,name='signup'),
    path('home/', views.homepage, name='homepage'),
    path('book/', views.create_booking_view, name='book_venue'),
    path('book/success/', views.booking_success_view, name='booking_success'),
    path('receipt/', views.receipt, name='confirmation'),
    path('my-admin/', views.custom_admin_dashboard, name='custom_admin'),
    path('my-admin/room/<int:room_id>/toggle/', views.toggle_room_status, name='toggle_room'),
    path('verify/', views.verify_reservation_view, name='verify_reservation'),
]