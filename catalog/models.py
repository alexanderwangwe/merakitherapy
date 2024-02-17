from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date


class Therapist(models.Model):
    therapist_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    SPECIALIZATION_CHOICES = [
        ('COUPLES', 'COUPLES'),
        ('TRAUMA', 'TRAUMA'),
        ('DEPRESSION', 'DEPRESSION'),
        ('NUTRITIONAL', 'NUTRITIONAL'),
        ('FAMILY', 'FAMILY'),
        ('BEHAVIORAL', 'BEHAVIORAL'),
        ('ADDICTION', 'ADDICTION'),
    ]
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES, blank=True,
                                      help_text="Select Specialization")

    AVAILABILITY_STATUS = (
        ('A', 'Available'),
        ('B', 'BOOKED')
    )

    availability = models.CharField(max_length=10, choices=AVAILABILITY_STATUS, blank=True, default="Available",
                                    help_text="Confirm Availability")

    class Meta:
        ordering = ['name', 'specialization']

        permissions = [
            ("can_mark_available", "Set therapist as available"),
            ("can_mark_booked", "Set therapist as booked"),
        ]

    def __str__(self):
        return (f"Therapist {self.name}, Contact: {self.contact}, Specialization: {self.specialization}, Availability: "
                f"{self.availability}")

    def get_absolute_url(self):
        return reverse('therapist-detail', args=[self.therapist_id])


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=15)

    class Meta:
        ordering = ['name']
        permissions = [
            ("can_add_appointment", "Can add appointment"),
        ]

    def __str__(self):
        return f"Patient {self.patient_id}: {self.name}"

    def calculate_age(self):
        today = date.today()
        birth_date = self.date_of_birth
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    @property
    def age(self):
        return self.calculate_age()

    def get_absolute_url(self):
        return reverse('patient-detail', args=[str(self.patient_id)])


# Appointment model
class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)

    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

    APPOINTMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES, default='Pending')
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    SERVICE_CHOICES = [
        ('COUPLES', 'COUPLES'),
        ('TRAUMA', 'TRAUMA'),
        ('DEPRESSION', 'DEPRESSION'),
        ('NUTRITIONAL', 'NUTRITIONAL'),
        ('FAMILY', 'FAMILY'),
        ('BEHAVIORAL', 'BEHAVIORAL'),
        ('ADDICTION', 'ADDICTION'),
    ]
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, blank=True,
                               help_text="Select Specialization")

    class Meta:
        ordering = ['date', 'time', 'therapist', 'patient', 'status']

    def __str__(self):
        patient_name = self.patient.name if self.patient else "Unassigned"
        return (f"Appointment {self.appointment_id} on {self.date} at {self.time} with {patient_name}, "
                f"Status: {self.status}")

    def get_absolute_url(self):
        return reverse('appointment-detail', args=[str(self.appointment_id)])
