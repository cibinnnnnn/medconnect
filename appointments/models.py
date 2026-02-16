from django.db import models
from accounts.models import Patient, Doctor

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    appointment_id = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    token_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.appointment_id} - {self.patient.user.get_full_name()} with Dr. {self.doctor.user.get_full_name()}"


class Prescription(models.Model):
    prescription_id = models.CharField(max_length=20, unique=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    diagnosis = models.TextField()
    medications = models.TextField(help_text="Medicine name, dosage, frequency")
    tests_recommended = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.prescription_id} - {self.patient.user.get_full_name()}"


class MedicalRecord(models.Model):
    record_id = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    record_type = models.CharField(max_length=50, choices=(
        ('lab_report', 'Lab Report'),
        ('imaging', 'Imaging'),
        ('prescription', 'Prescription'),
        ('consultation', 'Consultation'),
        ('other', 'Other'),
    ))
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='medical_records/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.record_id} - {self.title}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('appointment', 'Appointment'),
        ('prescription', 'Prescription'),
        ('report', 'Report'),
        ('reminder', 'Reminder'),
        ('general', 'General'),
    )
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
