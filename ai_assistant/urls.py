from django.urls import path
from .views import symptom_checker

urlpatterns = [

    path(
        'symptom-checker/',
        symptom_checker,
        name='symptom_checker'
    ),

]