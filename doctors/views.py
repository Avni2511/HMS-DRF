from rest_framework.viewsets import ModelViewSet
from .models import Doctor
from .serializers import DoctorSerializer
from accounts.permissions import IsAdmin


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdmin]
