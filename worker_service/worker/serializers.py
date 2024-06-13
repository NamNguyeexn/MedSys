from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password

# class FullNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FullName
#         fields = ['first_name', 'last_name']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city', 'province', 'hometown']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password']
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)

class StaffSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    account = AccountSerializer()
    position = PositionSerializer()

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'position', 'address', 'account', 'email', 'phone_number', 'cid', 'is_active' ]
    
    def update(self, instance, validated_data):
        position_data = validated_data.pop('position', None)
        address_data = validated_data.pop('address', None)
        account_data = validated_data.pop('account', None)

        
        if position_data:
            PositionSerializer().update(instance.position, position_data)
        if address_data:
            AddressSerializer().update(instance.address, address_data)
        if account_data:
            AccountSerializer().update(instance.account, account_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class StaffInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    position = PositionSerializer()

    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'position', 'address', 'phone_number', 'email', 'cid', 'is_active']

class StaffLoginSerializer(serializers.Serializer):
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
                staff = Staff.objects.filter(account=account.id).first()
                staff_serializer = StaffInfoSerializer(staff)
                return staff_serializer.data
            else:
                raise serializers.ValidationError('Invalid password.')
        else:
            raise serializers.ValidationError('Staff does not exist.')
