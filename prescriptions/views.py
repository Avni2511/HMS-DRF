from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from appointments.models import Appointment
from .models import Prescription


@login_required
def add_prescription(request, appointment_id):

    if request.user.role != 'doctor':

        messages.error(
            request,
            'Only doctors can add prescriptions'
        )

        return redirect('dashboard')

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    if request.method == 'POST':

        diagnosis = request.POST.get(
            'diagnosis'
        )

        medicines = request.POST.get(
            'medicines'
        )

        notes = request.POST.get(
            'notes'
        )

        Prescription.objects.create(

            appointment=appointment,

            diagnosis=diagnosis,

            medicines=medicines,

            notes=notes
        )

        messages.success(
            request,
            'Prescription Added Successfully'
        )

        return redirect(
            'appointment_list'
        )

    context = {

        'appointment': appointment
    }

    return render(
        request,
        'prescriptions/add.html',
        context
    )




@login_required
def prescription_list(request):

    if request.user.role != 'patient':

        messages.error(
            request,
            'Permission Denied'
        )

        return redirect('dashboard')

    patient = Patient.objects.get(
        user=request.user
    )

    prescriptions = Prescription.objects.filter(
        appointment__patient=patient
    ).order_by('-created_at')

    context = {

        'prescriptions': prescriptions
    }

    return render(
        request,
        'prescriptions/list.html',
        context
    )