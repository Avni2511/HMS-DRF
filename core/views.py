from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

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
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # check username exists
        if User.objects.filter(username=username).exists():

            messages.error(request, 'Username already exists')

            return redirect('register')

        # create user
        user = User.objects.create_user(

            username=username,
            password=password,
            role='patient'
        )

        # create patient profile
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

    return render(request, 'register.html')


# =========================
# HOME VIEW
# =========================
@login_required
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
@login_required
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

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')

        date = request.POST.get('date')

        time = request.POST.get('time')

        doctor = Doctor.objects.get(id=doctor_id)

        patient = Patient.objects.get(user=request.user)

        Appointment.objects.create(

            doctor=doctor,
            patient=patient,
            date=date,
            time=time,
            status='Pending'
        )

        messages.success(
            request,
            'Appointment Booked Successfully'
        )

        return redirect('appointment_list')

    context = {

        'doctors': doctors
    }

    return render(
        request,
        'appointments/book.html',
        context
    )