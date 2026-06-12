from django.urls import path
from .views import *

urlpatterns = [

    path(
        'add/<int:appointment_id>/',
        add_prescription,
        name='add_prescription'
    ),
    path(
    'my-prescriptions/',
    prescription_list,
    name='prescription_list'
),

]