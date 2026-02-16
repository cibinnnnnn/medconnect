import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from accounts.models import User, Patient, Doctor
from datetime import datetime

# Create admin user if not exists
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123',
        role='admin'
    )
    print(f"Created admin: {admin_user}")
else:
    print("Admin user already exists")

# Create a test doctor user if not exists
if not User.objects.filter(username='doctor1').exists():
    doctor_user = User.objects.create_user(
        username='doctor1',
        email='doctor@test.com',
        password='doctor123',
        first_name='John',
        last_name='Smith',
        phone='1234567890',
        address='123 Main St',
        date_of_birth=datetime(1980, 1, 1).date(),
        role='doctor'
    )
    print(f"Created doctor user: {doctor_user}")
    
    # Create doctor profile
    doctor = Doctor.objects.create(
        user=doctor_user,
        doctor_id='DOC001',
        specialization='cardiology',
        qualification='MBBS, MD Cardiology',
        experience_years=10,
        consultation_fee=50.00,
        available_days='Mon,Tue,Wed,Thu,Fri',
        is_available=True
    )
    print(f"Created doctor profile: {doctor}")
else:
    print("Doctor user already exists")

# Create a test patient user if not exists
if not User.objects.filter(username='patient1').exists():
    patient_user = User.objects.create_user(
        username='patient1',
        email='patient@test.com',
        password='patient123',
        first_name='Jane',
        last_name='Doe',
        phone='9876543210',
        address='456 Oak Ave',
        date_of_birth=datetime(1990, 5, 15).date(),
        role='patient'
    )
    print(f"Created patient user: {patient_user}")
    
    # Create patient profile
    patient = Patient.objects.create(
        user=patient_user,
        patient_id='PAT001',
        blood_group='O+',
        emergency_contact='9876543210'
    )
    print(f"Created patient profile: {patient}")
else:
    print("Patient user already exists")

print("\n✅ Test data ready!")
