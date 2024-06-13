from django.db import models

# Create your models here.
class ServiceInvoice(models.Model):
    staff_id = models.IntegerField()
    patient_id = models.PositiveIntegerField(null=True)
    created_at = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "service_invoices"


class Service(models.Model):
    name = models.TextField(max_length=255)

    class Meta:
        db_table = "services"


class ServiceInvoiceDetail(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_invoice = models.ForeignKey(ServiceInvoice, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    service_date = models.DateField(auto_now=True)

    class Meta:
        db_table = "service_invoice_details"


class MedicineInvoice(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    patient_id = models.IntegerField()
    staff_id = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "medicine_invoices"


class MedicineInvoiceDetail(models.Model):
    invoice = models.ForeignKey(MedicineInvoice, on_delete=models.CASCADE)
    medical_supply_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        db_table = "medicine_invoice_details"