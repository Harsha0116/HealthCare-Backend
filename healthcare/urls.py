from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('healthcare.apps.authentication.urls')),
    path('api/patients/', include('healthcare.apps.patients.urls')),
    path('api/doctors/', include('healthcare.apps.doctors.urls')),
    path('api/mappings/', include('healthcare.apps.mappings.urls')),
]
