import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from accounts.models import User, Doctor
from datetime import datetime

doctors_data = [
    {
        'username': 'doctor_smith',
        'password': 'Smith@123',
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john.smith@medconnect.com',
        'specialization': 'cardiology',
        'qualification': 'MBBS, MD Cardiology',
        'experience_years': 12,
        'consultation_fee': 75.00,
        'doctor_id': 'DOC001'
    },
    {
        'username': 'doctor_sarah',
        'password': 'Sarah@123',
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'email': 'sarah.johnson@medconnect.com',
        'specialization': 'pediatrics',
        'qualification': 'MBBS, MD Pediatrics',
        'experience_years': 8,
        'consultation_fee': 60.00,
        'doctor_id': 'DOC002'
    },
    {
        'username': 'doctor_mike',
        'password': 'Mike@123',
        'first_name': 'Michael',
        'last_name': 'Davis',
        'email': 'michael.davis@medconnect.com',
        'specialization': 'dermatology',
        'qualification': 'MBBS, MD Dermatology',
        'experience_years': 10,
        'consultation_fee': 65.00,
        'doctor_id': 'DOC003'
    },
    {
        'username': 'doctor_emma',
        'password': 'Emma@123',
        'first_name': 'Emma',
        'last_name': 'Wilson',
        'email': 'emma.wilson@medconnect.com',
        'specialization': 'neurology',
        'qualification': 'MBBS, MD Neurology',
        'experience_years': 15,
        'consultation_fee': 80.00,
        'doctor_id': 'DOC004'
    },
    {
        'username': 'doctor_alex',
        'password': 'Alex@123',
        'first_name': 'Alexander',
        'last_name': 'Brown',
        'email': 'alex.brown@medconnect.com',
        'specialization': 'orthopedics',
        'qualification': 'MBBS, MS Orthopedics',
        'experience_years': 11,
        'consultation_fee': 70.00,
        'doctor_id': 'DOC005'
    },
    {
        'username': 'doctor_lisa',
        'password': 'Lisa@123',
        'first_name': 'Lisa',
        'last_name': 'Martinez',
        'email': 'lisa.martinez@medconnect.com',
        'specialization': 'gynecology',
        'qualification': 'MBBS, MD Gynecology',
        'experience_years': 9,
        'consultation_fee': 65.00,
        'doctor_id': 'DOC006'
    },
    {
        'username': 'doctor_james',
        'password': 'James@123',
        'first_name': 'James',
        'last_name': 'Anderson',
        'email': 'james.anderson@medconnect.com',
        'specialization': 'general',
        'qualification': 'MBBS, General Medicine',
        'experience_years': 7,
        'consultation_fee': 50.00,
        'doctor_id': 'DOC007'
    },
    {
        'username': 'doctor_maria',
        'password': 'Maria@123',
        'first_name': 'Maria',
        'last_name': 'Garcia',
        'email': 'maria.garcia@medconnect.com',
        'specialization': 'psychiatry',
        'qualification': 'MBBS, MD Psychiatry',
        'experience_years': 13,
        'consultation_fee': 70.00,
        'doctor_id': 'DOC008'
    },
    {
        'username': 'doctor_robert',
        'password': 'Robert@123',
        'first_name': 'Robert',
        'last_name': 'Taylor',
        'email': 'robert.taylor@medconnect.com',
        'specialization': 'ent',
        'qualification': 'MBBS, MS ENT',
        'experience_years': 10,
        'consultation_fee': 60.00,
        'doctor_id': 'DOC009'
    },
    {
        'username': 'doctor_diane',
        'password': 'Diane@123',
        'first_name': 'Diane',
        'last_name': 'Thomas',
        'email': 'diane.thomas@medconnect.com',
        'specialization': 'ophthalmology',
        'qualification': 'MBBS, MD Ophthalmology',
        'experience_years': 12,
        'consultation_fee': 75.00,
        'doctor_id': 'DOC010'
    },
    {
        'username': 'doctor_david',
        'password': 'David@123',
        'first_name': 'David',
        'last_name': 'Moore',
        'email': 'david.moore@medconnect.com',
        'specialization': 'cardiology',
        'qualification': 'MBBS, MD Cardiology',
        'experience_years': 16,
        'consultation_fee': 85.00,
        'doctor_id': 'DOC011'
    }
]

print("\n" + "="*70)
print("CREATING DOCTOR ACCOUNTS".center(70))
print("="*70 + "\n")

created_count = 0
for idx, doctor_info in enumerate(doctors_data, 1):
    username = doctor_info['username']
    
    # Check if doctor already exists
    if User.objects.filter(username=username).exists():
        print(f"⚠️  Doctor '{username}' already exists - skipping")
        continue
    
    # Generate unique doctor ID
    doctor_count = Doctor.objects.count() + 1
    unique_doctor_id = f"DOC{doctor_count:03d}"
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=doctor_info['email'],
        password=doctor_info['password'],
        first_name=doctor_info['first_name'],
        last_name=doctor_info['last_name'],
        phone='9876543210',
        address='Medical Building, Main St',
        date_of_birth=datetime(1980, 1, 1).date(),
        role='doctor'
    )
    
    # Create doctor profile
    doctor = Doctor.objects.create(
        user=user,
        doctor_id=unique_doctor_id,
        specialization=doctor_info['specialization'],
        qualification=doctor_info['qualification'],
        experience_years=doctor_info['experience_years'],
        consultation_fee=doctor_info['consultation_fee'],
        available_days='Mon,Tue,Wed,Thu,Fri',
        is_available=True
    )
    
    created_count += 1
    print(f"✅ Created: {doctor_info['first_name']} {doctor_info['last_name']} ({doctor_info['specialization'].upper()})")

print("\n" + "="*70)
print("DOCTOR LOGIN CREDENTIALS".center(70))
print("="*70 + "\n")

for i, doctor_info in enumerate(doctors_data, 1):
    print(f"{i:2d}. Username: {doctor_info['username']:<20} | Password: {doctor_info['password']}")

print("\n" + "="*70)
print(f"✅ {created_count} doctors created successfully!".center(70))
print("="*70 + "\n")

print("📝 Access the admin panel at: http://127.0.0.1:8000/admin/")
print("📝 Login page at: http://127.0.0.1:8000/accounts/doctor-login/\n")
