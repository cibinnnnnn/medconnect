#!/usr/bin/env python
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')
django.setup()

from core.ai_utils import doctor_allocator
from accounts.models import User

def test_analytics_data():
    print("Testing Analytics Data Generation...")
    
    # Test workload analytics
    analytics = doctor_allocator.get_workload_analytics()
    print(f"Total doctors in analytics: {len(analytics)}")
    
    if analytics:
        print("\nSample analytics data:")
        for i, item in enumerate(analytics[:3]):
            doctor_name = item['doctor'].user.get_full_name() if item['doctor'] else "None"
            print(f"  {i+1}. Dr: {doctor_name}")
            print(f"     Workload: {item['workload']}")
            print(f"     Status: {item['status']}")
            print(f"     Utilization: {item['utilization_rate']:.1f}%")
    else:
        print("No analytics data found!")
    
    return analytics

def test_export_functions():
    print("\nTesting Export Functions...")
    
    # Test CSV export
    try:
        from core.views import export_analytics_csv
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        factory = RequestFactory()
        request = factory.get('/export/analytics/csv/')
        
        # Create admin user for testing
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            request.user = admin_user
            
            # Test the function
            response = export_analytics_csv(request)
            print(f"CSV Export Status: {response.status_code}")
            print(f"CSV Content Type: {response.get('Content-Type')}")
            print(f"CSV Filename: {response.get('Content-Disposition')}")
        else:
            print("No admin user found for testing")
    except Exception as e:
        print(f"CSV Export Error: {e}")
    
    # Test Excel export
    try:
        from core.views import export_analytics_excel
        
        request = factory.get('/export/analytics/excel/')
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            request.user = admin_user
            
            response = export_analytics_excel(request)
            print(f"Excel Export Status: {response.status_code}")
            print(f"Excel Content Type: {response.get('Content-Type')}")
            print(f"Excel Filename: {response.get('Content-Disposition')}")
        else:
            print("No admin user found for testing")
    except Exception as e:
        print(f"Excel Export Error: {e}")
    
    # Test PDF export
    try:
        from core.views import export_analytics_pdf
        
        request = factory.get('/export/analytics/pdf/')
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            request.user = admin_user
            
            response = export_analytics_pdf(request)
            print(f"PDF Export Status: {response.status_code}")
            print(f"PDF Content Type: {response.get('Content-Type')}")
            print(f"PDF Filename: {response.get('Content-Disposition')}")
        else:
            print("No admin user found for testing")
    except Exception as e:
        print(f"PDF Export Error: {e}")

if __name__ == "__main__":
    analytics = test_analytics_data()
    test_export_functions()
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
