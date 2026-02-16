from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-doctors/', views.manage_doctors, name='manage_doctors'),
    path('manage-patients/', views.manage_patients, name='manage_patients'),
    path('analytics/', views.analytics, name='analytics'),
    path('export/analytics/csv/', views.export_analytics_csv, name='export_analytics_csv'),
    path('export/analytics/excel/', views.export_analytics_excel, name='export_analytics_excel'),
    path('export/analytics/pdf/', views.export_analytics_pdf, name='export_analytics_pdf'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
