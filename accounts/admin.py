from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'date_of_birth', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'date_of_birth')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
