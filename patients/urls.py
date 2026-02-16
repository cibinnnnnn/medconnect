from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('medical-history/', views.medical_history, name='medical_history'),
    path('diagnostic-reports/', views.diagnostic_reports, name='diagnostic_reports'),
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('qr-code/', views.qr_code_view, name='qr_code'),
]
