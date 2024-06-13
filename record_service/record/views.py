import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MedicalRecord
from .serializer import MedicalRecordSerializer

class RecordCreateAPIView(APIView):
    def post(self, request):
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordDetailAPIView(APIView):
    
    def get_patient_info(self, patient_id):
        url = f'http://127.0.0.1:8000/api/patient/{patient_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_doctor_info(self, doctor_id):
        url = f'http://127.0.0.1:8003/api/doctor/{doctor_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get(self, request, id):
        medical_record = get_object_or_404(MedicalRecord, id=id)
        patient_info = self.get_patient_info(medical_record.patient_id)
        doctor_info = self.get_doctor_info(medical_record.doctor_id)
        serializer = MedicalRecordSerializer(medical_record)
        data = serializer.data
        if patient_info:
            data['patient_info'] = patient_info
        if doctor_info:
            data['doctor_info'] = doctor_info
        data.pop('patient_id', None)
        data.pop('doctor_id', None)
        return Response(data)

class RecordUpdateAPIView(APIView):
    def put(self, request, id):
        medical_record = get_object_or_404(MedicalRecord, id=id)
        serializer = MedicalRecordSerializer(medical_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordListByPatientOrDoctorAPIView(APIView):
    def get_patient_info(self, patient_id):
        url = f'http://127.0.0.1:8000/api/patient/{patient_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_doctor_info(self, doctor_id):
        url = f'http://127.0.0.1:8003/api/doctor/{doctor_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get(self, request):
        role = request.GET.get('role')
        id = request.GET.get('id')
        if role == 'patient':
            queryset = MedicalRecord.objects.filter(patient_id=id)
        elif role == 'doctor':
            queryset = MedicalRecord.objects.filter(doctor_id=id)
        else:
            return Response({"detail": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MedicalRecordSerializer(queryset, many=True)
        data_list = serializer.data
        for data in data_list:
            patient_info = self.get_patient_info(data['patient_id'])
            doctor_info = self.get_doctor_info(data['doctor_id'])
            if patient_info:
                data['patient_info'] = patient_info
            if doctor_info:
                data['doctor_info'] = doctor_info
            data.pop('patient_id', None)
            data.pop('doctor_id', None)
        return Response(data_list)

class RecordSearchAPIView(APIView):
    def get_patient_info(self, patient_id):
        url = f'http://127.0.0.1:8000/api/patient/{patient_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_doctor_info(self, doctor_id):
        url = f'http://127.0.0.1:8003/api/doctor/{doctor_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get(self, request, patient_id):
        keywords = request.GET.get('keywords', '')
        queryset = MedicalRecord.objects.filter(patient_id=patient_id, reason__icontains=keywords)
        serializer = MedicalRecordSerializer(queryset, many=True)
        data_list = serializer.data
        for data in data_list:
            patient_info = self.get_patient_info(data['patient_id'])
            doctor_info = self.get_doctor_info(data['doctor_id'])
            if patient_info:
                data['patient_info'] = patient_info
            if doctor_info:
                data['doctor_info'] = doctor_info
            data.pop('patient_id', None)
            data.pop('doctor_id', None)
        return Response(data_list)