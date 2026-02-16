from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-records/', views.patient_records, name='patient_records'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('prescription/create/<int:appointment_id>/', views.create_prescription, name='create_prescription'),
    path('appointments/', views.manage_appointments, name='manage_appointments'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment_status, name='update_appointment_status'),
]
