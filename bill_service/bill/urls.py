from django.urls import path
from .views import (
    ServiceInvoiceCreateAPIView,
    ServiceInvoiceUpdateAPIView,
    ServiceInvoiceDetailAPIView,
    ServiceInvoiceListByPatientOrStaffAPIView,
    MedicineInvoiceCreateAPIView,
    MedicineInvoiceUpdateAPIView,
    MedicineInvoiceDetailAPIView,
    MedicineInvoiceListByPatientOrStaffAPIView
)

urlpatterns = [
    path('api/payment/services/create', ServiceInvoiceCreateAPIView.as_view(), name='service-invoice-create'),
    path('api/payment/service/update/<int:service_invoice_id>', ServiceInvoiceUpdateAPIView.as_view(), name='service-invoice-update'),
    path('api/payment/service/<int:service_invoice_id>', ServiceInvoiceDetailAPIView.as_view(), name='service-invoice-detail'),
    path('api/payment/service', ServiceInvoiceListByPatientOrStaffAPIView.as_view(), name='service-invoice-list'),

    path('api/payment/medicine/create', MedicineInvoiceCreateAPIView.as_view(), name='medicine-invoice-create'),
    path('api/payment/medicine/update/<int:medicine_invoice_id>', MedicineInvoiceUpdateAPIView.as_view(), name='medicine-invoice-update'),
    path('api/payment/medicine/<int:medicine_invoice_id>', MedicineInvoiceDetailAPIView.as_view(), name='medicine-invoice-detail'),
    path('api/payment/medicine', MedicineInvoiceListByPatientOrStaffAPIView.as_view(), name='medicine-invoice-list'),
]