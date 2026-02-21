from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'specialization_display', 'license_number',
            'phone', 'email', 'hospital', 'years_of_experience', 'qualifications',
            'bio', 'is_available', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_license_number(self, value):
        instance = self.instance
        qs = Doctor.objects.filter(license_number=value)
        if instance:
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise serializers.ValidationError('A doctor with this license number already exists.')
        return value


class DoctorListSerializer(serializers.ModelSerializer):
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'specialization_display', 'hospital', 'is_available', 'created_at']
