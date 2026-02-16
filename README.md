# MedConnect - AI-Driven Healthcare Management Platform

![MedConnect Logo](static/images/logo.png)

## 🏥 Project Overview

MedConnect is a comprehensive AI-driven healthcare assistance and management platform that bridges the gap between patients, doctors, and hospital administration. It enables secure access to medical records, smart appointment scheduling, AI-based symptom analysis, and efficient communication — fostering a patient-centered digital healthcare ecosystem.

## ✨ Key Features

### Patient Module
- **AI-Powered Symptom Checker** 🤖 - NLP-based symptom analysis with TF-IDF and confidence scoring
- **Smart Doctor Recommendations** - AI-driven doctor allocation with load balancing
- **Personal Medical History Management** - View and manage consultation records, diagnoses, and treatments
- **Access Diagnostic Reports & Prescriptions** - Download lab results, imaging reports, and prescriptions
- **Intelligent Appointment Booking** - AI recommends best-fit doctors based on symptoms and workload
- **QR Live Booking** - Quick registration via QR code scanning at hospitals
- **Notifications & Reminders** - Real-time alerts for appointments and reports

### Doctor Module
- **Patient Record Access** - View detailed medical history and reports
- **Consultation & Prescription Management** - Digital prescriptions and diagnosis recording
- **Smart Appointment Management** - AI-balanced schedules for optimal workload
- **Secure Communication** - Internal messaging with admin
- **Performance Dashboard** - Analytics and consultation metrics

### Admin Module
- **AI Workload Analytics** 📊 - Real-time doctor load balancing and utilization tracking
- **Doctor & Department Management** - Add/update doctors and assign specializations
- **Patient Record Oversight** - Manage patient profiles and records
- **Smart Resource Allocation** - AI-powered appointment distribution
- **Reports & Analytics** - Comprehensive performance reports with AI insights
- **Role & Access Management** - Control user permissions and security

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend:** Python, Django 4.2
- **Database:** SQLite (easily upgradeable to PostgreSQL/MySQL)
- **AI/ML:** TensorFlow 2.15, Scikit-learn 1.3, NLTK 3.8
- **NLP:** Natural Language Processing with TF-IDF vectorization
- **Additional:** QR Code Generation, REST API support, Smart Algorithms

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional)

## 🚀 Installation & Setup

### 1. Navigate to Project Directory

```powershell
cd "c:\Users\aisha\OneDrive\Desktop\WISTORA\MedConnect"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter execution policy errors, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note:** This includes AI/ML libraries (TensorFlow, Scikit-learn, NLTK) which may take a few minutes to install.

### 5. Initialize AI Components

NLTK data will download automatically on first run. To download manually:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 6. Run Database Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Create Media and Static Directories

```powershell
New-Item -ItemType Directory -Path "media" -Force
New-Item -ItemType Directory -Path "media/profiles" -Force
New-Item -ItemType Directory -Path "media/qr_codes" -Force
New-Item -ItemType Directory -Path "media/medical_records" -Force
```

### 9. Collect Static Files

```powershell
python manage.py collectstatic --noinput
```

### 9. Run Development Server

```powershell
python manage.py runserver
```

### 10. Access the Application

Open your web browser and navigate to:
- **Homepage:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## 👥 User Roles & Access

### Patient
- Register via the homepage
- Access patient dashboard
- Book appointments
- Use AI symptom checker
- View medical history and reports
- Download QR code for quick check-in

### Doctor
- Created by admin via Django admin panel
- Access doctor dashboard
- Manage appointments
- View patient records
- Create prescriptions

### Admin
- Created via `createsuperuser` command
- Full system access
- Manage doctors and patients
- View analytics and reports
- System configuration

## 📱 Creating Sample Data

### Creating a Doctor Account:

1. Login to admin panel: http://127.0.0.1:8000/admin/
2. Go to **Users** → **Add User**
3. Create username and password
4. Set **Role** to "Doctor"
5. Fill in other details
6. Save the user
7. Go to **Doctors** → **Add Doctor**
8. Select the user you just created
9. Fill in specialization, qualification, and availability
10. Save

### Creating Test Appointments:

Appointments can be created by:
- Patients booking through the website
- Admin creating via Django admin panel

## 🎨 Customization

### Update Site Information

Edit `core/views.py` to customize:
- Department listings
- Testimonials
- Contact information

### Modify Styles

Edit `static/css/style.css` for visual customization.

### Change Color Scheme

Update CSS variables in `style.css`:
```css
:root {
    --primary-color: #4A90E2;
    --secondary-color: #50C878;
    --dark-color: #2C3E50;
}
```

## 🤖 AI Features

### NLP-Based Symptom Checker
MedConnect uses advanced Natural Language Processing to analyze patient symptoms:
- **TF-IDF Vectorization**: Converts symptom descriptions into numerical features
- **Cosine Similarity**: Matches symptoms against medical knowledge base
- **12 Specializations**: Cardiology, Neurology, Orthopedics, and more
- **Confidence Scoring**: 0-100% accuracy indication
- **Severity Assessment**: Automatic urgency level detection (Low/Moderate/High)
- **Personalized Advice**: Age and gender-specific recommendations

**Example Usage:**
```python
from core.ai_utils import symptom_analyzer

result = symptom_analyzer.analyze_symptoms(
    "I have severe chest pain and shortness of breath",
    patient_age=45,
    patient_gender="Male"
)
# Returns: specialization, severity, confidence, recommendations
```

### Smart Doctor Allocation
AI-powered load balancing system that optimizes doctor assignments:
- **Multi-Factor Scoring**: Specialization match (40%), Workload (40%), Availability (20%)
- **Load Balancing**: Tracks 7-day appointment forecast
- **Workload Analytics**: Real-time utilization monitoring (0-100%)
- **Alternative Suggestions**: Provides backup doctor options
- **Admin Dashboard**: Visual workload distribution and alerts

**Example Usage:**
```python
from core.ai_utils import doctor_allocator

allocation = doctor_allocator.allocate_doctor(
    patient,
    required_specialization="cardiology",
    preferred_date=today
)
# Returns: recommended doctor, score, workload, alternatives
```

### AI Technical Stack
- **NLTK**: Text preprocessing, tokenization, stopword removal
- **Scikit-learn**: TF-IDF vectorization, cosine similarity
- **TensorFlow**: Ready for deep learning models (future)
- **Pandas & NumPy**: Data manipulation and numerical operations

**For detailed AI documentation, see:** [AI_FEATURES.md](AI_FEATURES.md)

## 🔒 Security Notes

**Important for Production:**

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Update `ALLOWED_HOSTS`
4. Use PostgreSQL or MySQL instead of SQLite
5. Configure proper email backend
6. Set up HTTPS
7. Configure secure cookie settings
8. Set up proper backup procedures

## 📊 Database Models

### Core Models:
- **User** - Extended Django user with role-based access
- **Patient** - Patient-specific information and QR code
- **Doctor** - Doctor profile with specialization
- **Appointment** - Appointment scheduling and management
- **Prescription** - Medical prescriptions
- **MedicalRecord** - Diagnostic reports and documents
- **Notification** - Real-time alerts system

## 🧪 Testing the Application

### Test Patient Flow:
1. Register as a new patient
2. Complete profile information
3. Use AI symptom checker
4. Book an appointment
5. View your QR code
6. Check notifications

### Test Doctor Flow:
1. Login as doctor
2. View dashboard
3. Check today's appointments
4. View patient records
5. Create prescriptions

### Test Admin Flow:
1. Login to admin dashboard
2. Add new doctors
3. View analytics
4. Manage appointments
5. Export reports

## 🐛 Troubleshooting

### Issue: Module not found errors
**Solution:** Ensure virtual environment is activated and all dependencies are installed

### Issue: Database errors
**Solution:** Run migrations again:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution:** Run collectstatic:
```powershell
python manage.py collectstatic --noinput
```

### Issue: QR codes not generating
**Solution:** Ensure qrcode package is installed:
```powershell
pip install qrcode[pil]
```

## 📚 API Documentation

REST API endpoints are available for mobile app integration:
- `/api/patients/` - Patient management
- `/api/doctors/` - Doctor information
- `/api/appointments/` - Appointment booking
- `/api/prescriptions/` - Prescription access

## 🤝 Contributing

This project was developed as a healthcare management solution. For improvements:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is developed for educational and healthcare purposes.

## 📞 Support

For issues or questions:
- Email: info@medconnect.com
- Phone: +1 (555) 123-4567

## 🎯 Future Enhancements

- [ ] Video consultation integration
- [ ] Payment gateway for consultation fees
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Advanced AI diagnosis
- [ ] Telemedicine features
- [ ] Integration with wearable devices
- [ ] Prescription delivery tracking

## 👨‍💻 Development Team

Developed with ❤️ by the WISTORA Team

---

**Version:** 1.0.0  
**Last Updated:** December 2025

## Quick Start Commands

```powershell
# Setup
cd "c:\Users\aisha\OneDrive\Desktop\WISTORA\MedConnect"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

Enjoy using MedConnect! 🏥✨
