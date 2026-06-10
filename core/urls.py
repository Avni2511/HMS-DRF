from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    # LOGIN PAGE FIRST
    path('login/', login_view, name='login'),
    # REGISTER
    path('register/', register_view, name='register'),

    # DASHBOARD
    path('', dashboard, name='dashboard'),

    path('logout/', logout_view, name='logout'),
    # HOME
    path('home/', home, name='home'),

    # DOCTORS
    path('doctors/', doctor_list, name='doctor_list'),

    # APPOINTMENTS
    path('appointments/', appointment_list, name='appointment_list'),

    # BOOK APPOINTMENT
    path('appointments/book/', book_appointment, name='book_appointment'),

    path(
    'appointment/<int:appointment_id>/approve/',
    approve_appointment,
    name='approve_appointment'
),

    path(
    'appointment/<int:appointment_id>/cancel/',
    cancel_appointment,
    name='cancel_appointment'
),
]