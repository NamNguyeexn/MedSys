import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import ServiceInvoice, MedicineInvoice, ServiceInvoiceDetail, MedicineInvoiceDetail
from .serializer import ServiceInvoiceSerializer, MedicineInvoiceSerializer, ServiceInvoiceDetailSerializer, MedicineInvoiceDetailSerializer
from django.shortcuts import get_object_or_404

# Helper function to get patient data
def get_patient_data(patient_id):
    response = requests.get(f'http://127.0.0.1:8000/api/patient/{patient_id}/')
    if response.status_code == 200:
        return response.json()
    return None

# Helper function to get staff data
def get_staff_data(staff_id):
    response = requests.get(f'http://127.0.0.1:8004/api/staff/{staff_id}/')
    if response.status_code == 200:
        return response.json()
    return None

# Tạo hóa đơn dịch vụ
class ServiceInvoiceCreateAPIView(APIView):
    def post(self, request):
        patient_id = request.data.get('patient_id')
        staff_id = request.data.get('staff_id')
        
        patient_data = get_patient_data(patient_id)
        staff_data = get_staff_data(staff_id)

        if not patient_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not staff_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ServiceInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Cập nhật hóa đơn dịch vụ
class ServiceInvoiceUpdateAPIView(APIView):
    def put(self, request, service_invoice_id):
        service_invoice = get_object_or_404(ServiceInvoice, pk=service_invoice_id)
        
        patient_id = request.data.get('patient_id')
        staff_id = request.data.get('staff_id')
        
        patient_data = get_patient_data(patient_id)
        staff_data = get_staff_data(staff_id)

        if not patient_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not staff_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ServiceInvoiceSerializer(service_invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy thông tin hóa đơn dịch vụ
class ServiceInvoiceDetailAPIView(APIView):
    def get(self, request, service_invoice_id):
        service_invoice = get_object_or_404(ServiceInvoice, pk=service_invoice_id)
        serializer = ServiceInvoiceSerializer(service_invoice)
        return Response(serializer.data)

# Lấy danh sách hóa đơn dịch vụ theo ID bệnh nhân hoặc ID nhân viên
class ServiceInvoiceListByPatientOrStaffAPIView(APIView):
    def get(self, request):
        role = request.query_params.get('role')
        user_id = request.query_params.get('id')
        
        if role == 'patient':
            patient_data = get_patient_data(user_id)
            if not patient_data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            invoices = ServiceInvoice.objects.filter(patient_id=user_id)
        elif role == 'staff':
            staff_data = get_staff_data(user_id)
            if not staff_data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            invoices = ServiceInvoice.objects.filter(staff_id=user_id)
        else:
            invoices = ServiceInvoice.objects.none()
        
        serializer = ServiceInvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

# Tạo hóa đơn mua đồ
class MedicineInvoiceCreateAPIView(APIView):
    def post(self, request):
        patient_id = request.data.get('patient_id')
        staff_id = request.data.get('staff_id')
        
        patient_data = get_patient_data(patient_id)
        staff_data = get_staff_data(staff_id)

        if not patient_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not staff_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = MedicineInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Cập nhật hóa đơn mua đồ
class MedicineInvoiceUpdateAPIView(APIView):
    def put(self, request, medicine_invoice_id):
        medicine_invoice = get_object_or_404(MedicineInvoice, pk=medicine_invoice_id)
        
        patient_id = request.data.get('patient_id')
        staff_id = request.data.get('staff_id')
        
        patient_data = get_patient_data(patient_id)
        staff_data = get_staff_data(staff_id)

        if not patient_data:
            return Response({'error': 'Invalid patient_id'}, status=status.HTTP_400_BAD_REQUEST)
        if not staff_data:
            return Response({'error': 'Invalid staff_id'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MedicineInvoiceSerializer(medicine_invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lấy thông tin hóa đơn mua đồ
class MedicineInvoiceDetailAPIView(APIView):
    def get(self, request, medicine_invoice_id):
        medicine_invoice = get_object_or_404(MedicineInvoice, pk=medicine_invoice_id)
        serializer = MedicineInvoiceSerializer(medicine_invoice)
        return Response(serializer.data)

# Lấy danh sách hóa đơn mua đồ theo ID bệnh nhân hoặc ID nhân viên
class MedicineInvoiceListByPatientOrStaffAPIView(APIView):
    def get(self, request):
        role = request.query_params.get('role')
        user_id = request.query_params.get('id')
        
        if role == 'patient':
            patient_data = get_patient_data(user_id)
            if not patient_data:
                return Response({'error': 'Invalid patient_id'}, status=status.HTTP_400_BAD_REQUEST)
            invoices = MedicineInvoice.objects.filter(patient_id=user_id)
        elif role == 'staff':
            staff_data = get_staff_data(user_id)
            if not staff_data:
                return Response({'error': 'Invalid staff_id'}, status=status.HTTP_400_BAD_REQUEST)
            invoices = MedicineInvoice.objects.filter(staff_id=user_id)
        else:
            invoices = MedicineInvoice.objects.none()
        
        serializer = MedicineInvoiceSerializer(invoices, many=True)
        return Response(serializer.data)