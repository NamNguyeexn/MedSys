from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Doctor, Account
from .serializers import DoctorSerializer, AccountSerializer

class DoctorCreateAPIView(LoginRequiredMixin, APIView):
    login_url = '/admin/login/'

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorDetailAPIView(LoginRequiredMixin, APIView):
    login_url = '/admin/login/'

    def get(self, request, id):
        doctor = get_object_or_404(Doctor, id=id)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

class DoctorUpdateAPIView(LoginRequiredMixin, APIView):
    login_url = '/admin/login/'

    def put(self, request, id):
        doctor = get_object_or_404(Doctor, id=id)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorDeleteAPIView(LoginRequiredMixin, APIView):
    login_url = '/admin/login/'

    def delete(self, request, id):
        doctor = get_object_or_404(Doctor, id=id)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DoctorSearchAPIView(LoginRequiredMixin, APIView):
    login_url = '/admin/login/'

    def get(self, request):
        keywords = request.query_params.get('keywords', '')
        doctors = Doctor.objects.filter(
            Q(first_name__icontains=keywords) |
            Q(last_name__icontains=keywords) |
            Q(email__icontains=keywords) |  # Search by email
            Q(phone__icontains=keywords) |  # Search by phone number
            Q(cid__icontains=keywords) |    # Search by CID
            Q(department__name__icontains=keywords) |
            Q(address__street__icontains=keywords) |  # Search by street
            Q(address__district__icontains=keywords) |  # Search by district
            Q(address__city__icontains=keywords) |  # Search by city
            Q(address__province__icontains=keywords) |  # Search by province
            Q(address__hometown__icontains=keywords)  # Search by hometown
        )
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class DoctorLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Logged in successfully'})
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class DoctorLogoutAPIView(LoginRequiredMixin, APIView):
    login_url = '/admin/login/'

    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})

# def doctor_module(request):
#     return render(request, 'doctor/doctor_module.html')

# def view_patients(request):
#     patients = Patient.objects.all()
#     return render(request, 'doctor/view_patients.html', {'patients': patients})

# def search_patients(request):
#     return render(request, 'doctor/search_patients.html')