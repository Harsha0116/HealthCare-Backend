import uuid
from django.db import models


class PatientDoctorMapping(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='doctor_mappings',
    )
    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='patient_mappings',
    )
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient_doctor_mappings'
        unique_together = ['patient', 'doctor']
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.patient.name} -> Dr. {self.doctor.name}"
