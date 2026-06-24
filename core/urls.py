from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', home, name='home'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),

    path('dashboard/', dashboard, name='dashboard'),

    path('logout/', logout_view, name='logout'),

    path('doctors/', doctor_list, name='doctor_list'),

    path('appointments/', appointment_list, name='appointment_list'),

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