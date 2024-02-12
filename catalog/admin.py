from django.contrib import admin
from .models import Therapist, Patient, Appointment

# Register your models here.
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(Appointment)

