# MedConnect - Project Structure

```
MedConnect/
│
├── 📁 medconnect/                    # Main Django project
│   ├── __init__.py
│   ├── settings.py                   # Project settings & configuration
│   ├── urls.py                       # Main URL routing
│   ├── wsgi.py                       # WSGI configuration
│   └── asgi.py                       # ASGI configuration
│
├── 📁 accounts/                      # User authentication & profiles
│   ├── __init__.py
│   ├── admin.py                      # Admin configuration for User, Patient, Doctor
│   ├── apps.py                       # App configuration
│   ├── models.py                     # User, Patient, Doctor models
│   ├── forms.py                      # Registration & login forms
│   ├── views.py                      # Auth views (register, login, logout)
│   └── urls.py                       # Auth URLs
│
├── 📁 patients/                      # Patient module
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                     # Patient-specific models (if any)
│   ├── views.py                      # Patient dashboard, symptom checker, etc.
│   └── urls.py                       # Patient URLs
│
├── 📁 doctors/                       # Doctor module
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                     # Doctor-specific models (if any)
│   ├── views.py                      # Doctor dashboard, prescriptions, etc.
│   └── urls.py                       # Doctor URLs
│
├── 📁 appointments/                  # Appointments & prescriptions
│   ├── __init__.py
│   ├── admin.py                      # Appointment, Prescription admin
│   ├── apps.py
│   ├── models.py                     # Appointment, Prescription, MedicalRecord, Notification
│   ├── views.py                      # Appointment booking & management
│   └── urls.py                       # Appointment URLs
│
├── 📁 core/                          # Core functionality (homepage, admin)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py                      # Homepage, admin dashboard, analytics
│   └── urls.py                       # Core URLs
│
├── 📁 templates/                     # HTML templates
│   ├── base.html                     # Base template with navbar & footer
│   │
│   ├── 📁 core/                      # Core templates
│   │   ├── index.html               # Homepage
│   │   ├── about.html               # About page
│   │   ├── contact.html             # Contact page
│   │   ├── admin_dashboard.html     # Admin dashboard
│   │   ├── manage_doctors.html      # Manage doctors
│   │   ├── manage_patients.html     # Manage patients
│   │   └── analytics.html           # Analytics & reports
│   │
│   ├── 📁 accounts/                  # Authentication templates
│   │   ├── register.html            # Patient registration
│   │   └── login.html               # Login page
│   │
│   ├── 📁 patients/                  # Patient templates
│   │   ├── dashboard.html           # Patient dashboard
│   │   ├── symptom_checker.html     # AI symptom checker
│   │   ├── medical_history.html     # Medical history
│   │   ├── diagnostic_reports.html  # Reports & records
│   │   └── qr_code.html             # QR code page
│   │
│   ├── 📁 doctors/                   # Doctor templates
│   │   ├── dashboard.html           # Doctor dashboard
│   │   ├── patient_records.html     # Patient records list
│   │   ├── patient_detail.html      # Patient detail view
│   │   ├── create_prescription.html # Prescription creation
│   │   └── manage_appointments.html # Appointment management
│   │
│   └── 📁 appointments/              # Appointment templates
│       ├── book_appointment.html    # Book new appointment
│       ├── my_appointments.html     # Appointments list
│       └── appointment_detail.html  # Appointment details
│
├── 📁 static/                        # Static files (CSS, JS, images)
│   ├── 📁 css/
│   │   └── style.css                # Main stylesheet
│   │
│   ├── 📁 js/
│   │   └── main.js                  # JavaScript functionality
│   │
│   └── 📁 images/                    # Images (optional)
│       └── (logos, icons, etc.)
│
├── 📁 media/                         # User uploads
│   ├── 📁 profiles/                  # Profile pictures
│   ├── 📁 qr_codes/                  # Patient QR codes
│   └── 📁 medical_records/           # Medical reports & files
│
├── 📁 venv/                          # Virtual environment (created after setup)
│   └── (Python packages)
│
├── 📁 staticfiles/                   # Collected static files (production)
│   └── (generated by collectstatic)
│
├── 📄 manage.py                      # Django management script
├── 📄 requirements.txt               # Python dependencies
├── 📄 db.sqlite3                     # SQLite database (created after setup)
├── 📄 .gitignore                     # Git ignore file
│
├── 📄 setup.ps1                      # Automated setup script (PowerShell)
├── 📄 start.ps1                      # Quick start script (PowerShell)
│
├── 📄 README.md                      # Main documentation
├── 📄 QUICKSTART.md                  # Quick start guide
├── 📄 FEATURES.md                    # Feature documentation
├── 📄 DEPLOYMENT_CHECKLIST.md        # Production deployment guide
├── 📄 PROJECT_SUMMARY.md             # Project summary
└── 📄 PROJECT_STRUCTURE.md           # This file
```

---

## 📊 File Statistics

### Python Files
- **Models:** 4 files (User, Patient, Doctor, Appointment, etc.)
- **Views:** 5 files (Authentication, Patient, Doctor, Appointments, Core)
- **URLs:** 6 files (Main, Accounts, Patients, Doctors, Appointments, Core)
- **Admin:** 5 files (Configuration for all models)
- **Forms:** 1 file (Registration, Login)
- **Total:** 25+ Python files

### HTML Templates
- **Core:** 7 templates
- **Authentication:** 2 templates
- **Patient:** 5 templates
- **Doctor:** 5 templates
- **Appointments:** 3 templates
- **Base:** 1 template
- **Total:** 23 templates

### Static Files
- **CSS:** 1 file (style.css - 500+ lines)
- **JavaScript:** 1 file (main.js - 200+ lines)
- **Total:** 2 files

### Documentation
- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick start guide
- **FEATURES.md** - Feature documentation
- **DEPLOYMENT_CHECKLIST.md** - Production guide
- **PROJECT_SUMMARY.md** - Project overview
- **PROJECT_STRUCTURE.md** - This file
- **Total:** 6 documentation files

---

## 🎯 Key Components

### Database Models

```python
# accounts/models.py
- User (Extended AbstractUser)
  - role, phone, address, date_of_birth, profile_picture
- Patient (OneToOne with User)
  - patient_id, blood_group, emergency_contact, qr_code
- Doctor (OneToOne with User)
  - doctor_id, specialization, qualification, experience, fees

# appointments/models.py
- Appointment
  - appointment_id, patient, doctor, date, time, status, symptoms
- Prescription
  - prescription_id, appointment, diagnosis, medications
- MedicalRecord
  - record_id, patient, record_type, file
- Notification
  - user, notification_type, title, message, is_read
```

### URL Structure

```
/                                    → Homepage
/about/                              → About page
/contact/                            → Contact page
/accounts/register/                  → Patient registration
/accounts/login/                     → Login
/accounts/logout/                    → Logout
/accounts/dashboard/                 → Role-based redirect
/patients/dashboard/                 → Patient dashboard
/patients/symptom-checker/           → AI symptom checker
/patients/medical-history/           → Medical history
/patients/diagnostic-reports/        → Diagnostic reports
/patients/qr-code/                   → QR code page
/doctors/dashboard/                  → Doctor dashboard
/doctors/patient-records/            → Patient records
/doctors/patient/<id>/               → Patient detail
/doctors/prescription/create/<id>/   → Create prescription
/doctors/appointments/               → Manage appointments
/appointments/book/                  → Book appointment
/appointments/my-appointments/       → View appointments
/appointments/<id>/                  → Appointment detail
/appointments/<id>/cancel/           → Cancel appointment
/admin-dashboard/                    → Admin dashboard
/manage-doctors/                     → Manage doctors
/manage-patients/                    → Manage patients
/analytics/                          → Analytics & reports
/admin/                              → Django admin panel
```

---

## 🔧 Configuration Files

### settings.py - Key Settings
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',        # REST API
    'corsheaders',           # CORS handling
    'accounts',              # User management
    'patients',              # Patient module
    'doctors',               # Doctor module
    'appointments',          # Appointments
    'core',                  # Core functionality
]

AUTH_USER_MODEL = 'accounts.User'  # Custom user model
```

### requirements.txt - Dependencies
```
Django==4.2.7
Pillow==10.1.0
qrcode==7.4.2
python-decouple==3.8
djangorestframework==3.14.0
django-cors-headers==4.3.1
reportlab==4.0.7
openpyxl==3.1.2
openai==1.3.7
```

---

## 📝 Important Notes

### After Setup, You'll Have:
- ✅ Virtual environment in `venv/`
- ✅ Database `db.sqlite3`
- ✅ Media directories created
- ✅ Static files collected in `staticfiles/`
- ✅ Superuser account created

### Do NOT Commit to Git:
- `venv/` - Virtual environment
- `db.sqlite3` - Database
- `media/` - User uploads
- `staticfiles/` - Collected static files
- `*.pyc` - Compiled Python files
- `__pycache__/` - Python cache

### Always Keep:
- `.gitignore` - Git ignore rules
- `requirements.txt` - Dependencies list
- All documentation files
- Source code files

---

## 🚀 Quick Navigation

### For Development:
1. Start here: `README.md`
2. Quick setup: `QUICKSTART.md`
3. Understand features: `FEATURES.md`
4. Project layout: `PROJECT_STRUCTURE.md` (this file)

### For Deployment:
1. Security checklist: `DEPLOYMENT_CHECKLIST.md`
2. Production settings: `medconnect/settings.py`
3. Server configuration: External guides

### For Customization:
1. Templates: `templates/`
2. Styles: `static/css/style.css`
3. JavaScript: `static/js/main.js`
4. Views: Individual app `views.py` files
5. Models: Individual app `models.py` files

---

## 💡 Tips

### Finding What You Need:
- **Homepage design?** → `templates/core/index.html`
- **Patient dashboard?** → `templates/patients/dashboard.html`
- **User authentication?** → `accounts/views.py`
- **Database models?** → `*/models.py` files
- **URL routing?** → `*/urls.py` files
- **Admin config?** → `*/admin.py` files
- **Styles?** → `static/css/style.css`
- **JavaScript?** → `static/js/main.js`

### Common Modifications:
- **Change colors:** Edit CSS variables in `style.css`
- **Add new page:** Create template, add view, add URL
- **Modify dashboard:** Edit respective `dashboard.html`
- **Add new field:** Update model, make migrations
- **Change homepage content:** Edit `core/views.py` and `index.html`

---

**This structure ensures clean, maintainable, and scalable code organization!**

**Last Updated:** December 2025
