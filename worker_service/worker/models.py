from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)


class Address(models.Model):
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    hometown = models.CharField(max_length=255)

class Account(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)



class Staff(AbstractBaseUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    cid = models.CharField(unique=True, max_length=12)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def is_authenticated(self):
        return True
