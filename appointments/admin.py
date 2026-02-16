from django.contrib import admin
from .models import Appointment, Prescription, MedicalRecord, Notification

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('appointment_id', 'patient__user__username', 'doctor__user__username')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'patient', 'doctor', 'created_at')
    search_fields = ('prescription_id', 'patient__user__username')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'record_type', 'title', 'created_at')
    list_filter = ('record_type', 'created_at')
    search_fields = ('record_id', 'patient__user__username', 'title')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
