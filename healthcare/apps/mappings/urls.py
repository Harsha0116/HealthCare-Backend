from django.urls import path
from .views import MappingListCreateView, PatientDoctorsView, MappingDeleteView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<uuid:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),
    path('delete/<uuid:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
]
