from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from doctors.models import DoctorAvailability
from .utils import send_email_sendgrid

User = get_user_model()


# =========================
# LOGIN VIEW
# =========================
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'Invalid Username or Password'
            )

    return render(request, 'login.html')

def logout_view(request):

    logout(request)

    return redirect('login')


# =========================
# REGISTER VIEW
# PATIENT SELF REGISTRATION
# =========================
from django.db import IntegrityError

def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        age = request.POST.get('age')
        gender = request.POST.get('gender')

        print("USERNAME =", username)
        print("EMAIL =", email)

        # Username already exists
        if User.objects.filter(username__iexact=username).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return redirect('register')

        # Email already exists
        if User.objects.filter(email__iexact=email).exists():

            messages.error(
                request,
                'Email already exists'
            )

            return redirect('register')

        try:

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='patient'
            )

            Patient.objects.create(
                user=user,
                age=age,
                gender=gender
            )

            messages.success(
                request,
                'Patient Registered Successfully'
            )

            return redirect('login')

        except IntegrityError as e:

            print("INTEGRITY ERROR =", e)

            messages.error(
                request,
                'Username or Email already exists'
            )

            return redirect('register')

    return render(
        request,
        'register.html'
    )
# =========================
# HOME VIEW
# =========================

def home(request):

    return render(request, 'home.html')


# =========================
# DASHBOARD VIEW
# ROLE BASED DASHBOARD
# =========================
@login_required(login_url='login')
def dashboard(request):

    user = request.user

    # =====================
    # ADMIN DASHBOARD
    # =====================
    if user.role == 'admin':

        context = {

            'total_doctors': Doctor.objects.count(),

            'total_patients': Patient.objects.count(),

            'total_appointments': Appointment.objects.count(),

            'appointments': Appointment.objects.all().order_by('-id')[:5],

            'status_items': [

                {
                    'label': 'Database',
                    'value': 'Online',
                    'ok': True
                },

                {
                    'label': 'Booking System',
                    'value': 'Active',
                    'ok': True
                },

                {
                    'label': 'Notifications',
                    'value': 'Pending',
                    'ok': False
                },
            ]
        }

        return render(
            request,
            'dashboards/admin.html',
            context
        )

    # =====================
    # DOCTOR DASHBOARD
    # =====================
    elif user.role == 'doctor':

        doctor = Doctor.objects.get(user=user)

        appointments = Appointment.objects.filter(
            doctor=doctor
        )

        approved_count = appointments.filter(
            status='Approved'
        ).count()

        pending_count = appointments.filter(
            status='Pending'
        ).count()

        context = {

            'doctor': doctor,

            'appointments': appointments,

            'approved_count': approved_count,

            'pending_count': pending_count,
        }

        return render(
            request,
            'dashboards/doctor.html',
            context
        )

    # =====================
    # PATIENT DASHBOARD
    # =====================
    elif user.role == 'patient':

        patient = Patient.objects.get(user=user)

        appointments = Appointment.objects.filter(
            patient=patient
        )

        context = {

            'patient': patient,

            'appointments': appointments,
        }

        return render(
            request,
            'dashboards/patient.html',
            context
        )

    return redirect('login')


# =========================
# DOCTOR LIST
# =========================

def doctor_list(request):

    doctors = Doctor.objects.all()

    context = {

        'doctors': doctors
    }

    return render(
        request,
        'doctors/list.html',
        context
    )


# =========================
# APPOINTMENT LIST
# =========================
@login_required
def appointment_list(request):

    user = request.user

    # admin sees all
    if user.role == 'admin':

        appointments = Appointment.objects.all()

    # doctor sees own
    elif user.role == 'doctor':

        doctor = Doctor.objects.get(user=user)

        appointments = Appointment.objects.filter(
            doctor=doctor
        )

    # patient sees own
    else:

        patient = Patient.objects.get(user=user)

        appointments = Appointment.objects.filter(
            patient=patient
        )

    context = {

        'appointments': appointments
    }

    return render(
        request,
        'appointments/list.html',
        context
    )


# =========================
# BOOK APPOINTMENT
# =========================
@login_required
def book_appointment(request):

    # only patients can book
    if request.user.role != 'patient':

        messages.error(
            request,
            'Only patients can book appointments'
        )

        return redirect('dashboard')

    doctors = Doctor.objects.all()

    availability = DoctorAvailability.objects.all()

    if request.method == 'POST':
        

        doctor_id = request.POST.get('doctor')

        date = request.POST.get('date')

        time = request.POST.get('time')

        doctor = Doctor.objects.get(
            id=doctor_id
        )

        patient = Patient.objects.get(
            user=request.user
        )

        appointment = Appointment.objects.create(

            doctor=doctor,
            patient=patient,
            date=date,
            time=time,
            status='Pending'
        )

        # EMAIL NOTIFICATION
        try:
            send_email_sendgrid(
                to_email=request.user.email,
                subject="Appointment Booked Successfully",
                message=f"""
            Hello {request.user.username},

            Your appointment has been booked successfully.

            Doctor: Dr. {doctor.user.username}
            Date: {date}
            Time: {time}

            Status: Pending

            Thank you.
            """
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

        messages.success(
            request,
            'Appointment Booked Successfully'
        )

        return redirect('appointment_list')

    context = {

        'doctors': doctors,
        'availability': availability
    }

    return render(
        request,
        'appointments/book.html',
        context
    )

@login_required
def approve_appointment(request, appointment_id):

    if request.user.role not in ['admin', 'doctor']:

        messages.error(
            request,
            'Permission Denied'
        )

        return redirect('dashboard')

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    if request.user.role == 'doctor':

        doctor = Doctor.objects.get(
            user=request.user
        )

        if appointment.doctor != doctor:

            messages.error(
                request,
                'Permission Denied'
            )

            return redirect('appointment_list')

    appointment.status = 'Approved'
    appointment.save()

    messages.success(
        request,
        'Appointment Approved Successfully'
    )

    return redirect('appointment_list')

@login_required
def cancel_appointment(request, appointment_id):

    if request.user.role not in ['admin', 'doctor']:

        messages.error(
            request,
            'Permission Denied'
        )

        return redirect('dashboard')

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    # Doctor can cancel only their own appointments
    if request.user.role == 'doctor':

        doctor = Doctor.objects.get(
            user=request.user
        )

        if appointment.doctor != doctor:

            messages.error(
                request,
                'Permission Denied'
            )

            return redirect('appointment_list')

    appointment.status = 'Cancelled'

    appointment.save()

    messages.success(
        request,
        'Appointment Cancelled Successfully'
    )

    return redirect('appointment_list')