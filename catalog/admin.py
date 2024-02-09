from django.contrib import admin
from .models import Therapist, Patient, Appointment

# Register your models here.
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(Appointment)

#class TherapistAdmin(admin.ModelAdmin):
#admin.site.register(Therapist, TherapistAdmin)


#class PatientAdmin(admin.ModelAdmin):
    #list_display = ('name', 'gender', 'contact')
    #pass
#padmin.site.register(Patient, PatientAdmin)


#class AppointmentAdmin(admin.ModelAdmin):
   # pass
#admin.site.register(Appointment, AppointmentAdmin)