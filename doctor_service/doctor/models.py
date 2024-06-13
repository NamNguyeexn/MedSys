from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    street = models.TextField(max_length=255)
    district = models.TextField(max_length=255)
    city = models.TextField(max_length=255)
    province = models.TextField(max_length=255)
    hometown = models.TextField(max_length=255)

    class Meta:
        db_table = "addresses"


class Department(models.Model):
    name = models.TextField(max_length=255)

    class Meta:
        db_table = "departments"


class Doctor(models.Model):
    first_name = models.TextField(max_length=255)
    last_name = models.TextField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    phone = models.CharField(unique=True, max_length=255)
    cid = models.CharField(unique=True, max_length=12)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = "doctors"


class Account(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = "accounts"