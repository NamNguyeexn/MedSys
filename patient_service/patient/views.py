from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth.hashers import make_password
from .models import *
from django.db import transaction
from django.db.models import Q
import requests
class PatientCreateAPIView(APIView):
    @transaction.atomic
    def post(self, request):
        patient_data = request.data
        username = patient_data.get('username',{})
        check = Account.objects.filter(username=username).first()

        if check is not None:
            return Response({"message": "Tài khoản đã tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        patient_data['password'] = make_password(patient_data.get('password'))
        serializer = AccountSerializer(data=patient_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Thêm tài khỏa thành công"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.validated_data  
            patient_serializer = PatientInfoSerializer(patient)           
            return Response({
                'message':'Đăng nhập thành công',
                'patient': patient_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientListAPIView(APIView):
    def get(self, request):
        patients = Patient.objects.filter(is_active=1)
        serializers =  PatientInfoSerializer(patients, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK)    
class PatientListByDoctorAPIView(APIView):
    def get(self, request, doctor_id):
        response = requests.get("http://127.0.0.1:8001/api/records?role=doctor&id="+doctor_id)
        if response.status_code == 200:
            medical_records = response.json()
            patients = []
            for medical_record in medical_records:
                patient = Patient.objects.filter(pk=medical_record['patient_id'], is_active=1).first()
                if patient not in patients and patient is not None:
                    patients.append(patient)
            serializers = PatientInfoSerializer(patients, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)    
        else:
            patients = []
            serializers = PatientInfoSerializer(patients, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK) 
class PatientDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Patient.objects.get(pk=id,is_active=1)
        except Patient.DoesNotExist:
            return None
        
    def get(self, request,id):
        patient = self.get_object(id)
        if patient is None:
            return Response({"message":"Bệnh nhân không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientInfoSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
class PatientUpdateAPIView(APIView):
    def get_object(self, id):
        try:
            return Patient.objects.get(pk=id,is_active=1)
        except Patient.DoesNotExist:
            return None
    @transaction.atomic
    def put(self, request, id):
        patient = self.get_object(id)
        if patient is None:
            return Response({"message":"Bệnh nhân không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class PatientDeleteAPIView(APIView):
    def get_object(self, id):
        try:
            return Patient.objects.get(pk=id,is_active=1)
        except Patient.DoesNotExist:
            return None
    def delete(self, request, id):
        patient = self.get_object(id)
        if patient is None:
            return Response({"message":"Bệnh nhân không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        try:
            patient.is_active = 0
            patient.save()
            return Response({"message": "Bệnh nhân đã được xóa"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": f"Lỗi khi xóa bệnh nhân: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class PatientSearchAPIView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keywords','')
        patients = []
        if keyword:
            if keyword.isdigit():
                id_keyword = int(keyword)
                patient_query = Patient.objects.filter(Q(id=id_keyword))
                print(patient_query)
                if patient_query is not None:
                    patients.extend(patient_query)
            patient_list = Patient.objects.all()
            for patient in patient_list:
                name = patient.first_name+" "+ patient.last_name
                print(name)
                if name.lower().find(keyword.lower()) != -1 or keyword.lower().find(name.lower()) != -1:
                    if patient not in patient_list:
                        patients.append(patient)        
            adress = Address.objects.all()
            for ar in adress:
                if keyword.lower().find(ar.hometown.lower()) != -1 or keyword.lower().find(ar.street.lower()) !=-1 or keyword.lower().find(ar.city.lower()) !=-1 or keyword.lower().find(ar.district.lower()) !=-1 or keyword.lower().find(ar.province.lower()) !=-1:
                    patient = Patient.objects.filter(address=ar.id).first()
                    if patient not in patients:
                        patients.append(patient)   
        serializers = PatientInfoSerializer(patients, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)