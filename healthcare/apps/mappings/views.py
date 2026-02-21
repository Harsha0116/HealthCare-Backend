from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from healthcare.utils import success_response
from healthcare.apps.patients.models import Patient
from .models import PatientDoctorMapping
from .serializers import MappingSerializer, PatientDoctorDetailSerializer


class MappingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mappings = PatientDoctorMapping.objects.all().select_related('patient', 'doctor')
        serializer = MappingSerializer(mappings, many=True)
        return success_response(
            data={'count': mappings.count(), 'mappings': serializer.data},
            message='Mappings retrieved successfully.'
        )

    def post(self, request):
        serializer = MappingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=serializer.data,
            message='Doctor assigned to patient successfully.',
            status_code=status.HTTP_201_CREATED
        )


class PatientDoctorsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        if not Patient.objects.filter(id=patient_id).exists():
            return success_response(
                data=None,
                message='Patient not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        mappings = PatientDoctorMapping.objects.filter(patient_id=patient_id).select_related('doctor')
        serializer = PatientDoctorDetailSerializer(mappings, many=True)
        return success_response(
            data={'patient_id': str(patient_id), 'count': mappings.count(), 'doctors': serializer.data},
            message='Patient doctors retrieved successfully.'
        )


class MappingDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            mapping = PatientDoctorMapping.objects.get(id=pk)
        except PatientDoctorMapping.DoesNotExist:
            return success_response(
                data=None,
                message='Mapping not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        mapping.delete()
        return success_response(message='Doctor removed from patient successfully.')
