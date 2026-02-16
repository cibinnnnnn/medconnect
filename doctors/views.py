from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment, Prescription, MedicalRecord
from accounts.models import Patient

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    doctor = request.user.doctor_profile
    today_appointments = Appointment.objects.filter(doctor=doctor, status='confirmed')[:10]
    total_patients = Appointment.objects.filter(doctor=doctor).values('patient').distinct().count()
    
    context = {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'total_consultations': Appointment.objects.filter(doctor=doctor, status='completed').count(),
        'pending_appointments': Appointment.objects.filter(doctor=doctor, status='pending').count(),
        'total_patients': total_patients,
    }
    
    return render(request, 'doctors/dashboard.html', context)


@login_required
def patient_records(request):
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient')
    
    # Get unique patients
    patient_ids = appointments.values_list('patient__id', flat=True).distinct()
    patients = Patient.objects.filter(id__in=patient_ids)
    
    return render(request, 'doctors/patient_records.html', {'patients': patients})


@login_required
def patient_detail(request, patient_id):
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    patient = get_object_or_404(Patient, id=patient_id)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
        'medical_records': medical_records,
    }
    
    return render(request, 'doctors/patient_detail.html', context)


@login_required
def create_prescription(request, appointment_id):
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = request.user.doctor_profile
    
    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        medications = request.POST.get('medications')
        tests_recommended = request.POST.get('tests_recommended', '')
        follow_up_date = request.POST.get('follow_up_date', None)
        notes = request.POST.get('notes', '')
        
        # Generate prescription ID
        prescription_count = Prescription.objects.count() + 1
        prescription_id = f"PRE{prescription_count:06d}"
        
        prescription = Prescription.objects.create(
            prescription_id=prescription_id,
            appointment=appointment,
            patient=appointment.patient,
            doctor=doctor,
            diagnosis=diagnosis,
            medications=medications,
            tests_recommended=tests_recommended,
            follow_up_date=follow_up_date if follow_up_date else None,
            notes=notes
        )
        
        # Update appointment status
        appointment.status = 'completed'
        appointment.save()
        
        messages.success(request, 'Prescription created successfully')
        return redirect('doctor_dashboard')
    
    return render(request, 'doctors/create_prescription.html', {'appointment': appointment})


@login_required
def manage_appointments(request):
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date', '-appointment_time')
    
    return render(request, 'doctors/manage_appointments.html', {'appointments': appointments})


@login_required
def update_appointment_status(request, appointment_id):
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        appointment.status = status
        appointment.save()
        
        messages.success(request, f'Appointment status updated to {status}')
    
    return redirect('manage_appointments')
