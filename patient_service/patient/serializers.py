from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','street', 'district', 'city', 'province','hometown']
    
class PatientInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'address', 'date_of_birth','gender', 'phone_number', 'email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True) 

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')

        account = Account.objects.filter(username=username).first()
        if account:
            if check_password(password, account.password):
                patient = account.patient
                patient_serializer = PatientInfoSerializer(patient)
                return patient_serializer.data
            else:
                raise serializers.ValidationError('Invalid password.')
        else:
            raise serializers.ValidationError('Patient does not exist.')

class PatientUpdateInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'address','date_of_birth','gender', 'phone_number', 'email']

class PatientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Patient
        fields = ['id', 'first_name','last_name', 'address','date_of_birth', 'phone_number', 'gender','email']
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_instance = Address.objects.create(**address_data)
        patient_instance = Patient.objects.create(address=address_instance, **validated_data)
        return patient_instance
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address_instance = instance.address
        for attr, value in address_data.items():
            setattr(address_instance, attr, value)
        address_instance.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
class AccountSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'patient']
        
    def create(self, validated_data):
        patient_data = validated_data.pop('patient')
        patient_serializer = PatientSerializer(data=patient_data)
        if patient_serializer.is_valid():
            patient_instance = patient_serializer.save()
            account_instance = Account.objects.create(patient=patient_instance, **validated_data)
            return account_instance
        else:
            raise serializers.ValidationError("Invalid Patient data.")
    