import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Appointment
from .serializers import AppointmentSerializer
from django.utils.dateparse import parse_date

class AppointmentCreateAPIView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentDetailAPIView(APIView):
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
        appointment = get_object_or_404(Appointment, id=id)
        patient_info = self.get_patient_info(appointment.patient_id)
        doctor_info = self.get_doctor_info(appointment.doctor_id)
        serializer = AppointmentSerializer(appointment)
        data = serializer.data
        if patient_info:
            data['patient_info'] = patient_info
        if doctor_info:
            data['doctor_info'] = doctor_info
        data.pop('patient_id', None)
        data.pop('doctor_id', None)
        return Response(data)

class AppointmentUpdateAPIView(APIView):
    def put(self, request, id):
        appointment = get_object_or_404(Appointment, id=id)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentDeleteAPIView(APIView):
    def delete(self, request, id):
        appointment = get_object_or_404(Appointment, id=id)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentListByDoctorOrPatientAPIView(APIView):
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
            queryset = Appointment.objects.filter(patient_id=id)
        elif role == 'doctor':
            queryset = Appointment.objects.filter(doctor_id=id)
        else:
            return Response({"detail": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AppointmentSerializer(queryset, many=True)
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

class AppointmentListByDoctorOrPatientAndDateAPIView(APIView):
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
        role = request.query_params.get('role')
        entity_id = request.query_params.get('id')
        date = request.query_params.get('date')

        if role and entity_id:
            if role.lower() == 'doctor':
                appointments = Appointment.objects.filter(doctor_id=entity_id)
            elif role.lower() == 'patient':
                appointments = Appointment.objects.filter(patient_id=entity_id)
            else:
                return Response({"detail": "Invalid role provided"}, status=status.HTTP_400_BAD_REQUEST)

            if date:
                parsed_date = parse_date(date)
                if parsed_date:
                    appointments = appointments.filter(date=parsed_date)
                else:
                    return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = AppointmentSerializer(appointments, many=True)
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
        
        return Response({"detail": "Role and id are required parameters"}, status=status.HTTP_400_BAD_REQUEST)
