from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from healthcare.utils import success_response
from .models import Doctor
from .serializers import DoctorSerializer, DoctorListSerializer


class DoctorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = Doctor.objects.all().select_related('created_by')
        serializer = DoctorListSerializer(doctors, many=True)
        return success_response(
            data={'count': doctors.count(), 'doctors': serializer.data},
            message='Doctors retrieved successfully.'
        )

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return success_response(
            data=serializer.data,
            message='Doctor created successfully.',
            status_code=status.HTTP_201_CREATED
        )


class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, doctor_id):
        try:
            return Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return success_response(
                data=None,
                message='Doctor not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = DoctorSerializer(doctor)
        return success_response(data=serializer.data, message='Doctor retrieved successfully.')

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return success_response(
                data=None,
                message='Doctor not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        if doctor.created_by != request.user:
            return success_response(
                data=None,
                message='You do not have permission to update this doctor.',
                status_code=status.HTTP_403_FORBIDDEN
            )
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message='Doctor updated successfully.')

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return success_response(
                data=None,
                message='Doctor not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )
        if doctor.created_by != request.user:
            return success_response(
                data=None,
                message='You do not have permission to delete this doctor.',
                status_code=status.HTTP_403_FORBIDDEN
            )
        doctor.delete()
        return success_response(message='Doctor deleted successfully.')
