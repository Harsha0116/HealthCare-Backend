"""Serializers for Patients app."""
from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    created_by = serializers.StringRelatedField(read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'date_of_birth', 'age', 'gender', 'blood_group',
            'phone', 'email', 'address', 'medical_history', 'allergies',
            'emergency_contact_name', 'emergency_contact_phone',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_age(self, obj):
        from datetime import date
        today = date.today()
        dob = obj.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def validate_date_of_birth(self, value):
        from datetime import date
        if value >= date.today():
            raise serializers.ValidationError('Date of birth must be in the past.')
        return value


class PatientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing patients."""
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'date_of_birth', 'age', 'gender', 'blood_group', 'phone', 'created_at']

    def get_age(self, obj):
        from datetime import date
        today = date.today()
        dob = obj.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
