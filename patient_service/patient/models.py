from django.db import models

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.TextField(max_length=255)
    district = models.TextField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.TextField(max_length=255)
    hometown = models.TextField(max_length=255)
    class Meta:
        db_table = 'addresses'

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    is_active = models.IntegerField(default=1)
    class Meta:
        db_table = 'patients'

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    class Meta:
        db_table = 'accounts'