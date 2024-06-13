# from django.db import models

# # Create your models here.
# class Department(models.Model):
#     name = models.CharField(max_length=255)

# class Clinic(models.Model):
#     name = models.CharField(max_length=255)
#     department = models.ForeignKey(Department, related_name='clinics', on_delete=models.CASCADE)

# class HospitalRoom(models.Model):
#     number = models.CharField(max_length=50)
#     department = models.ForeignKey(Department, related_name='hospital_rooms', on_delete=models.CASCADE)

# class Bed(models.Model):
#     number = models.CharField(max_length=50)
#     hospital_room = models.ForeignKey(HospitalRoom, related_name='beds', on_delete=models.CASCADE)

from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "departments"


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    doctor_id = models.IntegerField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='clinics')

    class Meta:
        db_table = "clinics"


class Type(models.Model):
    name = models.CharField(max_length=255)  # Đổi từ TextField sang CharField
    price_per_day = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "types"


class Room(models.Model):
    number = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms', null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = "rooms"


class Bed(models.Model):
    number = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds', null=True)

    class Meta:
        db_table = "beds"


class PatientBed(models.Model):
    patient_id = models.IntegerField()
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='patient_beds', null=True)
    from_date = models.DateField()
    to_date = models.DateField()  # Sử dụng DateField cho sự nhất quán

    class Meta:
        db_table = "patients_beds"
