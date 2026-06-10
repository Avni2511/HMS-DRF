from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Doctor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    specialization = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    def __str__(self):

        return self.user.username


# ===================================
# DOCTOR AVAILABILITY
# ===================================

class DoctorAvailability(models.Model):

    DAYS = (

        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),

    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=20,
        choices=DAYS
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    def __str__(self):

        return (
            f"{self.doctor.user.username}"
            f" - {self.day}"
        )