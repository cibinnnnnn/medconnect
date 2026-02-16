from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor

# accounts/forms.py - Complete rewrite needed
class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    blood_group = forms.ChoiceField(
        choices=Patient.BLOOD_GROUP_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'date_of_birth', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
