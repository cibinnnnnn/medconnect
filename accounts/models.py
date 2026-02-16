from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Patient(models.Model):
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=20, unique=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    medical_conditions = models.TextField(blank=True, help_text="Chronic conditions, allergies, etc.")
    insurance_number = models.CharField(max_length=50, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.patient_id}"


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('general', 'General Medicine'),
        ('psychiatry', 'Psychiatry'),
        ('ophthalmology', 'Ophthalmology'),
        ('ent', 'ENT'),
        ('gynecology', 'Gynecology'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_days = models.CharField(max_length=100, help_text="e.g., Mon,Tue,Wed")
    available_time_start = models.TimeField(null=True, blank=True)
    available_time_end = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_specialization_display()}"
