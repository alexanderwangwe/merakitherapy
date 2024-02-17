from django import forms
from .models import Patient, Appointment, Therapist


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'gender', 'contact']


class TherapistRegistrationForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['name', 'contact', 'specialization', 'availability']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['therapist', 'patient', 'date', 'time', 'service']
