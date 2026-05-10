from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username