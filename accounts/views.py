from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientRegistrationForm, UserLoginForm
from .models import Patient
import qrcode
from io import BytesIO
from django.core.files import File

def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create patient profile
            patient_id = f"P{user.id:06d}"
            patient = Patient.objects.create(
                user=user,
                patient_id=patient_id,
                blood_group=form.cleaned_data.get('blood_group', '')
            )
            
            # Generate QR Code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"MedConnect-Patient-{patient_id}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            patient.qr_code.save(f'qr_{patient_id}.png', File(buffer), save=True)
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Redirect based on role
                if user.role == 'patient':
                    return redirect('patient_dashboard')
                elif user.role == 'doctor':
                    return redirect('doctor_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def doctor_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.role == 'doctor':
                    login(request, user)
                    return redirect('doctor_dashboard')
                else:
                    messages.error(request, 'Only doctors can access this login page')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/doctor_login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


@login_required
def dashboard(request):
    if request.user.role == 'patient':
        return redirect('patient_dashboard')
    elif request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('index')
