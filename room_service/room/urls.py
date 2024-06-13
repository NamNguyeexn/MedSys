from django.urls import path
from .views import ClinicListCreate, ClinicDetail, ClinicByDepartment, HospitalRoomListCreate, HospitalRoomDetail, HospitalRoomByDepartment, BedListCreate, BedDetail, BedByRoom, DepartmentListCreate, DepartmentDetail, PatientBedListCreate, PatientBedDetail


urlpatterns = [
    path('departments', DepartmentListCreate.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department-detail'),

    path('clinics', ClinicListCreate.as_view(), name='clinic-list-create'),
    path('clinics/<int:pk>/', ClinicDetail.as_view(), name='clinic-detail'),
    path('clinics/department/<int:department_id>/', ClinicByDepartment.as_view(), name='clinic-by-department'),
    
    path('rooms', HospitalRoomListCreate.as_view(), name='hospitalroom-list-create'),
    path('rooms/<int:pk>/', HospitalRoomDetail.as_view(), name='hospitalroom-detail'),
    path('rooms/department/<int:department_id>/', HospitalRoomByDepartment.as_view(), name='hospitalroom-by-department'),
    
    path('beds', BedListCreate.as_view(), name='bed-list-create'),
    path('beds/<int:pk>/', BedDetail.as_view(), name='bed-detail'),
    path('beds/room/<int:room_id>/', BedByRoom.as_view(), name='bed-by-room'),

     path('patient_beds', PatientBedListCreate.as_view(), name='patient_bed_list_create'),
    path('patient_beds/patient/<int:pk>/', PatientBedDetail.as_view(), name='patient_bed_detail'),
]
