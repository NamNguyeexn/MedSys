from django.contrib import admin
from django.urls import path
from appointment_service.appointment.views import (
    AppointmentCreateAPIView,
    AppointmentDetailAPIView,
    AppointmentUpdateAPIView,
    AppointmentDeleteAPIView,
    AppointmentListByDoctorOrPatientAPIView,
    AppointmentListByDoctorOrPatientAndDateAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appointments/patients/create', AppointmentCreateAPIView.as_view(), name='appointment-create'),
    path('appointments/<int:id>', AppointmentDetailAPIView.as_view(), name='appointment-detail'),
    path('appointments/update/<int:id>', AppointmentUpdateAPIView.as_view(), name='appointment-update'),
    path('appointments/delete/<int:id>', AppointmentDeleteAPIView.as_view(), name='appointment-delete'),
    path('appointments', AppointmentListByDoctorOrPatientAndDateAPIView.as_view(), name='appointment-list-by-doctor-or-patient-and-date'),
    path('appointments', AppointmentListByDoctorOrPatientAPIView.as_view(), name='appointment-list-by-doctor-or-patient'),
]
