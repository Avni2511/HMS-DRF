from rest_framework.viewsets import ModelViewSet
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.permissions import IsDoctor, IsPatient

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsDoctor | IsPatient]


def get_queryset(self):
    user = self.request.user

    if user.role == 'doctor':
        return Appointment.objects.filter(doctor__user=user)

    elif user.role == 'patient':
        return Appointment.objects.filter(patient__user=user)

    return Appointment.objects.all()