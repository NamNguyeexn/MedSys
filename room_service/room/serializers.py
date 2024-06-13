from rest_framework import serializers
from .models import Clinic, Room, Bed, Department, PatientBed

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'

class PatientBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientBed
        fields = '__all__'