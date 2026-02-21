from rest_framework import serializers

from healthcare.apps.patients.models import Patient
from healthcare.apps.doctors.models import Doctor
from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    patient_id = serializers.UUIDField(write_only=True)
    doctor_id = serializers.UUIDField(write_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient_id', 'doctor_id', 'patient_name', 'doctor_name',
            'doctor_specialization', 'notes', 'assigned_at', 'updated_at',
        ]
        read_only_fields = ['id', 'assigned_at', 'updated_at']

    def validate_patient_id(self, value):
        if not Patient.objects.filter(id=value).exists():
            raise serializers.ValidationError('Patient not found.')
        return value

    def validate_doctor_id(self, value):
        if not Doctor.objects.filter(id=value).exists():
            raise serializers.ValidationError('Doctor not found.')
        return value

    def validate(self, attrs):
        patient_id = attrs.get('patient_id')
        doctor_id = attrs.get('doctor_id')
        if patient_id and doctor_id:
            if PatientDoctorMapping.objects.filter(patient_id=patient_id, doctor_id=doctor_id).exists():
                raise serializers.ValidationError(
                    'This doctor is already assigned to this patient.'
                )
        return attrs

    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        doctor_id = validated_data.pop('doctor_id')
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        return PatientDoctorMapping.objects.create(patient=patient, doctor=doctor, **validated_data)


class PatientDoctorDetailSerializer(serializers.ModelSerializer):
    doctor_id = serializers.UUIDField(source='doctor.id', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)
    hospital = serializers.CharField(source='doctor.hospital', read_only=True)
    phone = serializers.CharField(source='doctor.phone', read_only=True)
    is_available = serializers.BooleanField(source='doctor.is_available', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'doctor_id', 'doctor_name', 'specialization', 'hospital', 'phone', 'is_available', 'notes', 'assigned_at']
