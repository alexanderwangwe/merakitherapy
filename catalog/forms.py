from django import forms
from .models import Patient, Appointment


class PatientRegistrationForm(forms.Form):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'gender', 'contact']


class TherapistAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'therapist', 'date', 'time', 'status']


