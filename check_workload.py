#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from core.ai_utils import doctor_allocator
from datetime import datetime, timedelta
from appointments.models import Appointment

def check_workload_calculation():
    print("=== Workload Calculation Analysis ===")
    
    # Check date range
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    print(f"Today: {today}")
    print(f"Next week: {next_week}")
    print(f"Date range: {today} to {next_week} (7 days)")
    
    # Check all appointments in this range
    upcoming = Appointment.objects.filter(
        appointment_date__gte=today,
        appointment_date__lte=next_week,
        status__in=['scheduled', 'confirmed']
    )
    
    print(f"\nUpcoming appointments in range: {upcoming.count()}")
    for apt in upcoming:
        print(f"  - {apt.doctor.user.get_full_name()}: {apt.appointment_date} ({apt.status})")
    
    # Check analytics results
    analytics = doctor_allocator.get_workload_analytics()
    print(f"\nAnalytics for {len(analytics)} doctors:")
    
    doctors_with_workload = [item for item in analytics if item['workload'] > 0]
    print(f"Doctors with workload > 0: {len(doctors_with_workload)}")
    
    for item in doctors_with_workload:
        doctor_name = item['doctor'].user.get_full_name()
        workload = item['workload']
        status = item['status']
        utilization = item['utilization_rate']
        print(f"  - Dr. {doctor_name}: {workload} appointments ({status}, {utilization:.1f}% utilization)")
    
    # Verify calculation manually
    print("\n=== Manual Verification ===")
    for item in doctors_with_workload:
        doctor = item['doctor']
        manual_count = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gte=today,
            appointment_date__lte=next_week,
            status__in=['scheduled', 'confirmed']
        ).count()
        
        analytics_count = item['workload']
        match = "✅" if manual_count == analytics_count else "❌"
        print(f"  Dr. {doctor.user.get_full_name()}: Manual={manual_count}, Analytics={analytics_count} {match}")

if __name__ == "__main__":
    check_workload_calculation()
