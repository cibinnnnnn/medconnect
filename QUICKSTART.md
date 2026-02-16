# MedConnect - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Method 1: Using Setup Script (Recommended)

1. **Open PowerShell** in the project directory:
   ```powershell
   cd "c:\Users\aisha\OneDrive\Desktop\WISTORA\MedConnect"
   ```

2. **Allow script execution** (if needed):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Run the setup script**:
   ```powershell
   .\setup.ps1
   ```

4. **Follow the prompts** to create your admin account

5. **Start the server**:
   ```powershell
   .\start.ps1
   ```

6. **Open your browser** and visit: http://127.0.0.1:8000/

---

### Method 2: Manual Setup

1. **Create virtual environment**:
   ```powershell
   python -m venv venv
   ```

2. **Activate virtual environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```powershell
   python manage.py createsuperuser
   ```

6. **Create media directories**:
   ```powershell
   New-Item -ItemType Directory -Path "media/profiles" -Force
   New-Item -ItemType Directory -Path "media/qr_codes" -Force
   New-Item -ItemType Directory -Path "media/medical_records" -Force
   ```

7. **Run server**:
   ```powershell
   python manage.py runserver
   ```

---

## 👤 User Accounts

### Admin Account
- **Create**: `python manage.py createsuperuser`
- **Access**: http://127.0.0.1:8000/admin/
- **Capabilities**: Full system access, manage doctors, patients, view analytics

### Doctor Account
1. Login to admin panel
2. Create a new User with role="Doctor"
3. Create a Doctor profile linked to that user
4. Fill in specialization, fees, and availability

### Patient Account
- **Register**: Click "Register" on homepage
- **Fill form**: Username, email, name, phone, date of birth
- **Login**: Use credentials to access patient dashboard

---

## 📋 First Steps After Setup

### 1. Create Test Doctor
```
Admin Panel → Users → Add User
- Username: dr.smith
- Role: Doctor
- Password: (set password)
- First Name: John
- Last Name: Smith

Admin Panel → Doctors → Add Doctor
- User: dr.smith
- Doctor ID: DOC001
- Specialization: General Medicine
- Qualification: MD, MBBS
- Experience: 10 years
- Consultation Fee: 100.00
- Available Days: Mon,Tue,Wed,Thu,Fri
- Available Time: 9:00 AM - 5:00 PM
- Is Available: ✓
```

### 2. Register as Patient
```
Homepage → Register
- Fill in all required fields
- Submit registration
- Login with new credentials
```

### 3. Book Test Appointment
```
Patient Dashboard → Book Appointment
- Select doctor
- Choose date and time
- Describe symptoms
- Submit booking
```

### 4. Doctor Confirms Appointment
```
Doctor Dashboard → Manage Appointments
- View pending appointments
- Click "Confirm"
```

### 5. Create Prescription
```
Doctor Dashboard → Today's Appointments
- Click "Prescribe" for completed consultation
- Fill diagnosis, medications, tests
- Save prescription
```

---

## 🎯 Feature Checklist

### Patient Features ✓
- [x] Registration with auto QR code generation
- [x] Personal dashboard with statistics
- [x] Book appointments with doctors
- [x] AI symptom checker
- [x] View medical history
- [x] Access prescriptions
- [x] Download diagnostic reports
- [x] QR code for quick check-in
- [x] Real-time notifications

### Doctor Features ✓
- [x] Professional dashboard
- [x] View today's appointments
- [x] Access patient records
- [x] Create digital prescriptions
- [x] Manage appointment schedules
- [x] Update appointment status
- [x] View patient medical history

### Admin Features ✓
- [x] Comprehensive admin dashboard
- [x] Manage doctors and departments
- [x] Manage patient records
- [x] View appointment statistics
- [x] Department-wise analytics
- [x] Monthly appointment reports
- [x] Export capabilities (PDF, Excel, CSV)
- [x] Role and access management

---

## 🔍 Testing the Application

### Test Scenario 1: Patient Registration Flow
1. Go to homepage
2. Click "Register"
3. Fill in patient details
4. Submit registration
5. Check email for confirmation (if configured)
6. Login with credentials
7. View patient dashboard
8. Check QR code generation

### Test Scenario 2: Appointment Booking Flow
1. Login as patient
2. Click "Book Appointment"
3. Select a doctor
4. Choose date and time
5. Enter symptoms
6. Submit booking
7. Check notification
8. View in "My Appointments"

### Test Scenario 3: Doctor Consultation Flow
1. Login as doctor
2. View today's appointments
3. Click on patient to view details
4. Review patient history
5. Create prescription
6. Mark consultation as completed
7. Verify prescription in patient's record

### Test Scenario 4: AI Symptom Checker
1. Login as patient
2. Go to "Symptom Checker"
3. Enter symptoms (e.g., "fever, headache, body aches")
4. Submit for analysis
5. Review AI recommendations
6. Click to book appointment with suggested specialist

---

## 🛠️ Common Commands

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start server
python manage.py runserver

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Create a backup of database
Copy-Item "db.sqlite3" -Destination "db.sqlite3.backup"

# Access Django shell
python manage.py shell
```

---

## 📊 Sample Data Creation (Optional)

### Create Multiple Doctors via Django Shell
```python
python manage.py shell

from accounts.models import User, Doctor

# Create doctor user
user = User.objects.create_user(
    username='dr.jones',
    email='jones@medconnect.com',
    password='password123',
    first_name='Sarah',
    last_name='Jones',
    role='doctor'
)

# Create doctor profile
doctor = Doctor.objects.create(
    user=user,
    doctor_id='DOC002',
    specialization='cardiology',
    qualification='MD, Cardiologist',
    experience_years=15,
    consultation_fee=150.00,
    available_days='Mon,Wed,Fri',
    is_available=True
)

print(f"Created: {doctor}")
```

---

## 🎨 Customization Tips

### Change Site Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #4A90E2;  /* Main blue color */
    --secondary-color: #50C878; /* Green accent */
    --dark-color: #2C3E50;      /* Dark text */
}
```

### Update Hospital Information
Edit `templates/base.html` footer section
Edit `core/views.py` for homepage content

### Add New Department
Edit `core/views.py` → `index` function → `departments` list

---

## 📱 Access URLs

- **Homepage**: http://127.0.0.1:8000/
- **Patient Dashboard**: http://127.0.0.1:8000/patients/dashboard/
- **Doctor Dashboard**: http://127.0.0.1:8000/doctors/dashboard/
- **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **Book Appointment**: http://127.0.0.1:8000/appointments/book/
- **Symptom Checker**: http://127.0.0.1:8000/patients/symptom-checker/

---

## 🐛 Troubleshooting

### Issue: "No module named 'accounts'"
**Solution**: Run migrations first:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: 
```powershell
python manage.py collectstatic --noinput
```

### Issue: QR code not generating
**Solution**: Ensure media directory exists:
```powershell
New-Item -ItemType Directory -Path "media/qr_codes" -Force
```

### Issue: Can't access admin panel
**Solution**: Create superuser:
```powershell
python manage.py createsuperuser
```

---

## 📧 Support

For issues or questions, refer to:
- README.md for detailed documentation
- Django documentation: https://docs.djangoproject.com/
- Bootstrap documentation: https://getbootstrap.com/docs/

---

**Congratulations!** You're now ready to use MedConnect! 🎉

Start exploring the features and customize as needed for your requirements.
