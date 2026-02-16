from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Notification
from accounts.models import Doctor
from datetime import datetime

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        messages.error(request, 'Only patients can book appointments')
        return redirect('index')
    
    # Check if user has a patient profile
    from accounts.models import Patient
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, 'Please complete your patient profile before booking an appointment.')
        return redirect('patient_dashboard')
    
    # Get symptom analysis from session if available
    symptom_analysis = request.session.get('symptom_analysis', {})
    recommended_specialization = symptom_analysis.get('specialization', None)
    
    # Smart doctor allocation if specialization is known
    recommended_doctor = None
    allocation_info = None
    
    if recommended_specialization:
        from core.ai_utils import doctor_allocator
        from datetime import datetime
        preferred_date = datetime.now().date()
        
        allocation_result = doctor_allocator.allocate_doctor(
            patient,
            recommended_specialization,
            preferred_date
        )
        
        recommended_doctor = allocation_result.get('doctor')
        allocation_info = {
            'score': allocation_result.get('score'),
            'reason': allocation_result.get('reason'),
            'workload': allocation_result.get('workload'),
            'alternatives': allocation_result.get('alternatives', [])
        }
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms', symptom_analysis.get('symptoms', ''))
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        # Generate appointment ID
        appointment_count = Appointment.objects.count() + 1
        appointment_id = f"APT{appointment_count:06d}"
        
        # Create appointment
        appointment = Appointment.objects.create(
            appointment_id=appointment_id,
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            symptoms=symptoms,
            status='pending'
        )
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            notification_type='appointment',
            title='Appointment Booked',
            message=f'Your appointment with Dr. {doctor.user.get_full_name()} on {appointment_date} has been booked.'
        )
        
        # Clear symptom analysis from session
        # if 'symptom_analysis' in request.session:
        #     del request.session['symptom_analysis']
        
        messages.success(request, 'Appointment booked successfully!')
        return redirect('appointments:my_appointments')
    
    # Get all available doctors
    doctors = Doctor.objects.filter(is_available=True)
    
    context = {
        'doctors': doctors,
        'recommended_doctor': recommended_doctor,
        'allocation_info': allocation_info,
        'symptom_analysis': symptom_analysis
    }
    
    return render(request, 'appointments/book_appointment.html', context)


@login_required
def my_appointments(request):
    if request.user.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user.patient_profile)
    elif request.user.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user.doctor_profile)
    else:
        appointments = Appointment.objects.all()
    
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, 'You can only cancel your own appointments')
        return redirect('appointments:my_appointments')
    
    appointment.status = 'cancelled'
    appointment.save()
    
    messages.success(request, 'Appointment cancelled successfully')
    return redirect('appointments:my_appointments')
