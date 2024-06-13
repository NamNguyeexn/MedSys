from rest_framework import serializers
from .models import MedicalRecord, MedicalTest

class MedicalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ['id', 'name']

class MedicalRecordSerializer(serializers.ModelSerializer):
    medical_tests = MedicalTestSerializer(many=True)

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient_id', 'doctor_id', 'date', 'reason', 'symptoms',
            'first_diagnosis', 'medical_tests', 'final_diagnosis',
            'treatment_plan', 'note'
        ]

    def create(self, validated_data):
        medical_tests_data = validated_data.pop('medical_tests')
        medical_record = MedicalRecord.objects.create(**validated_data)
        for medical_test_data in medical_tests_data:
            medical_test = MedicalTest.objects.create(**medical_test_data)
            medical_record.medical_tests.add(medical_test)
        return medical_record

    def update(self, instance, validated_data):
        medical_tests_data = validated_data.pop('medical_tests')
        instance.patient_id = validated_data.get('patient_id', instance.patient_id)
        instance.doctor_id = validated_data.get('doctor_id', instance.doctor_id)
        instance.date = validated_data.get('date', instance.date)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.symptoms = validated_data.get('symptoms', instance.symptoms)
        instance.first_diagnosis = validated_data.get('first_diagnosis', instance.first_diagnosis)
        instance.final_diagnosis = validated_data.get('final_diagnosis', instance.final_diagnosis)
        instance.treatment_plan = validated_data.get('treatment_plan', instance.treatment_plan)
        instance.note = validated_data.get('note', instance.note)

        instance.medical_tests.clear()
        for medical_test_data in medical_tests_data:
            medical_test = MedicalTest.objects.create(**medical_test_data)
            instance.medical_tests.add(medical_test)
        instance.save()
        return instance
