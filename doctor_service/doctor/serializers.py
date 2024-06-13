from rest_framework import serializers
from .models import Address, Department, Doctor, Account
from django.contrib.auth.models import User

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        department_data = validated_data.pop('department')
        
        address = Address.objects.create(**address_data)
        department, created = Department.objects.get_or_create(name=department_data['name'])
        doctor = Doctor.objects.create(address=address, department=department, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        department_data = validated_data.pop('department')
        
        instance.address.street = address_data.get('street', instance.address.street)
        instance.address.district = address_data.get('district', instance.address.district)
        instance.address.city = address_data.get('city', instance.address.city)
        instance.address.province = address_data.get('province', instance.address.province)
        instance.address.hometown = address_data.get('hometown', instance.address.hometown)
        instance.address.save()

        department, created = Department.objects.get_or_create(name=department_data['name'])
        instance.department = department

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.cid = validated_data.get('cid', instance.cid)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        return instance

class AccountSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Account
        fields = ['doctor', 'username', 'password']

    def create(self, validated_data):
        doctor_data = validated_data.pop('doctor')
        doctor_serializer = DoctorSerializer(data=doctor_data)
        if doctor_serializer.is_valid():
            doctor = doctor_serializer.save()
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )
            account = Account.objects.create(doctor=doctor, user=user, **validated_data)
            return account
        else:
            raise serializers.ValidationError(doctor_serializer.errors)
