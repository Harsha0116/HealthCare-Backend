"""Views for Patients app."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from healthcare.utils import success_response
from .models import Patient
from .serializers import PatientSerializer, PatientListSerializer


class PatientListCreateView(APIView):
    """List all patients for the authenticated user or create a new patient."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user).select_related('created_by')
        serializer = PatientListSerializer(patients, many=True)
        return success_response(
            data={'count': patients.count(), 'patients': serializer.data},
            message='Patients retrieved successfully.'
        )

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return success_response(
            data=serializer.data,
            message='Patient created successfully.',
            status_code=status.HTTP_201_CREATED
        )


class PatientDetailView(APIView):
    """Retrieve, update, or delete a specific patient."""
    permission_classes = [IsAuthenticated]

    def get_object(self, patient_id, user):
        try:
            return Patient.objects.get(id=patient_id, created_by=user)
        except Patient.DoesNotExist:
            return None

    def get(self, request, pk):
        patient = self.get_object(pk, request.user)
        if not patient:
            return success_response(
                data=None,
                message='Patient not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = PatientSerializer(patient)
        return success_response(data=serializer.data, message='Patient retrieved successfully.')

    def put(self, request, pk):
        patient = self.get_object(pk, request.user)
        if not patient:
            return success_response(
                data=None,
                message='Patient not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Patient updated successfully.')

    def delete(self, request, pk):
        patient = self.get_object(pk, request.user)
        if not patient:
            return success_response(
                data=None,
                message='Patient not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        patient.delete()
        return success_response(message='Patient deleted successfully.')
