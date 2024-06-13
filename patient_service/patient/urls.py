from django.urls import path
from .views import *
urlpatterns = [
    path('patients/create', PatientCreateAPIView.as_view(), name='register'),
    path('patients/login', PatientLoginAPIView.as_view(), name='login'),
    path('patients', PatientListAPIView.as_view(), name='get-all'),
    path('patients/<int:id>', PatientDetailAPIView.as_view(), name='patient-detail'),
    path('patients/update/<int:id>', PatientUpdateAPIView.as_view(), name='patient-update'),
    path('patients/delete/<int:id>', PatientDeleteAPIView.as_view(), name='patient-delete'),
    path('patients/doctors/<int:doctor_id>',PatientListByDoctorAPIView.as_view(), name='patient-doctor'),
    path('patients/search',PatientSearchAPIView.as_view(), name='search'),
]