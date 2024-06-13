from django.db import models

# Create your models here.
class Appointment(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    title = models.TextField(max_length=255)
    note = models.TextField(max_length=255)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = "appointments"