from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment, MedicalRecord, Prescription, Notification
from accounts.models import Doctor
import json

@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    patient = request.user.patient_profile
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:5]
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    
    context = {
        'patient': patient,
        'appointments': appointments,
        'notifications': notifications,
        'total_appointments': Appointment.objects.filter(patient=patient).count(),
        'upcoming_appointments': Appointment.objects.filter(patient=patient, status='confirmed').count(),
    }
    
    return render(request, 'patients/dashboard.html', context)


@login_required
def medical_history(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    patient = request.user.patient_profile
    appointments = Appointment.objects.filter(patient=patient, status='completed')
    prescriptions = Prescription.objects.filter(patient=patient)
    
    context = {
        'appointments': appointments,
        'prescriptions': prescriptions,
    }
    
    return render(request, 'patients/medical_history.html', context)


@login_required
def diagnostic_reports(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    patient = request.user.patient_profile
    records = MedicalRecord.objects.filter(patient=patient)
    
    return render(request, 'patients/diagnostic_reports.html', {'records': records})


@login_required
def symptom_checker(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    ai_response = None
    
        # Check if there's previous analysis in session
    if 'symptom_analysis' in request.session and request.method == 'GET':
        session_data = request.session['symptom_analysis']
        ai_response = {
        'message': f"Previous analysis: {session_data['specialization'].replace('_', ' ').title()} specialist (Confidence: {int(session_data['confidence'] * 100)}%).",
        'specialization': session_data['specialization'].replace('_', ' ').title(),
        'severity': session_data['severity'],
        'confidence': session_data['confidence'],
        'matched_symptoms': session_data.get('matched_symptoms', []),
        'recommendations': session_data.get('recommendations', ['This is your previous analysis. Submit new symptoms for updated analysis.']),
        'alternative_specializations': session_data.get('alternative_specializations', [])
    }
    
    if request.method == 'POST':
        from core.ai_utils import symptom_analyzer
        from datetime import date
        
        symptoms = request.POST.get('symptoms', '')
        
        # Get patient information for better analysis
        patient = request.user.patient_profile
        patient_age = None
        
        if patient and request.user.date_of_birth:
            today = date.today()
            patient_age = today.year - request.user.date_of_birth.year - (
                (today.month, today.day) < (request.user.date_of_birth.month, request.user.date_of_birth.day)
            )
        
        # Use AI analyzer for NLP-based symptom analysis
        analysis_result = symptom_analyzer.analyze_symptoms(
            symptoms,
            patient_age=patient_age,
            patient_gender=None
        )
        
        # Format specialization for display
        specialization_display = analysis_result['recommended_specialization'].replace('_', ' ').title()
        
        # Store analysis in session for booking
        request.session['symptom_analysis'] = {
        'symptoms': symptoms,
        'specialization': analysis_result['recommended_specialization'],
        'severity': analysis_result['severity'],
        'confidence': analysis_result['confidence'],
        'matched_symptoms': analysis_result.get('matched_symptoms', []),
        'recommendations': analysis_result.get('recommendations', []),
        'alternative_specializations': analysis_result.get('alternative_specializations', [])
}
        
        ai_response = {
            'message': f"Based on your symptoms, we recommend consulting a {specialization_display} specialist (Confidence: {int(analysis_result['confidence'] * 100)}%).",
            'specialization': specialization_display,
            'severity': analysis_result['severity'],
            'confidence': analysis_result['confidence'],
            'matched_symptoms': analysis_result.get('matched_symptoms', []),
            'recommendations': analysis_result['recommendations'],
            'alternative_specializations': [
                spec.replace('_', ' ').title() 
                for spec in analysis_result.get('alternative_specializations', [])
            ]
        }
    
    return render(request, 'patients/symptom_checker.html', {'ai_response': ai_response})


@login_required
def qr_code_view(request):
    if request.user.role != 'patient':
        messages.error(request, 'Access denied')
        return redirect('index')
    
    patient = request.user.patient_profile
    return render(request, 'patients/qr_code.html', {'patient': patient})

