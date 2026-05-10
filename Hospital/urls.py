from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from doctors.views import DoctorViewSet
from patients.views import PatientViewSet
from appointments.views import AppointmentViewSet

# DRF ROUTER
router = DefaultRouter()
router.register('doctors', DoctorViewSet)
router.register('patients', PatientViewSet)
router.register('appointments', AppointmentViewSet)

urlpatterns = [

    # ADMIN PANEL
    path('admin/', admin.site.urls),

    # CORE APP URLS
    path('', include('core.urls')),

    # LOGOUT
    # path(
    # 'logout/',
    # auth_views.LogoutView.as_view(
    #     next_page='/login/'
    # ),
    # name='logout'
    # ),

    # DRF API
    path('api/', include(router.urls)),
]