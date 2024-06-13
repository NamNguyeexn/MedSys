from rest_framework import serializers

from .models import ServiceInvoice, ServiceInvoiceDetail, Service, MedicineInvoice, MedicineInvoiceDetail

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceInvoice
        fields = '__all__'

class ServiceInvoiceDetailSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = ServiceInvoiceDetail
        fields = '__all__'

class MedicineInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineInvoice
        fields = '__all__'
        
class MedicineInvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineInvoiceDetail
        fields = '__all__'