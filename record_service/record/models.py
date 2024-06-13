from django.db import models

class MedicalTest(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'medical_tests'

class MedicalRecord(models.Model):
    patient_id = models.CharField(max_length=255)
    doctor_id = models.CharField(max_length=255)
    date = models.DateField()
    reason = models.CharField(max_length=255)
    symptoms = models.CharField(max_length=255)
    first_diagnosis = models.CharField(max_length=255)
    medical_tests = models.ManyToManyField(MedicalTest)
    final_diagnosis = models.CharField(max_length=255)
    treatment_plan = models.CharField(max_length=255)
    note = models.TextField()

    class Meta:
        db_table = 'medical_records'
