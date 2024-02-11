# catalog/views.py
from django.shortcuts import render
from django.views import generic
from django.views import View
from .models import Appointment, Patient, Therapist


def index(request):
    # Generate counts of some of the main objects
    num_appointments = Appointment.objects.all().count()
    num_patients = Patient.objects.all().count()
    num_therapists = Therapist.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template catalog/index.html with the data in the context variable.
    return render(request, 'catalog/index.html',
                  context={
                      'num_appointments': num_appointments,
                      'num_patients': num_patients,
                      'num_therapists': num_therapists,
                      'num_visits': num_visits,
                  },
                  )


class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = 'catalog/appointment_list.html'
    context_object_name = 'appointments'


class AppointmentDetailView(generic.DetailView):
    model = Appointment
    template_name = 'catalog/appointment_detail.html'
    context_object_name = 'appointment'


class PatientListView(generic.ListView):
    model = Patient
    template_name = 'catalog/patient_list.html'
    context_object_name = 'patients'


class PatientDetailView(generic.DetailView):
    model = Patient
    template_name = 'catalog/patient_detail.html'
    context_object_name = 'patient'


class TherapistListView(generic.ListView):
    model = Therapist
    template_name = 'catalog/therapist_list.html'
    context_object_name = 'therapists'


class TherapistDetailView(generic.DetailView):
    model = Therapist
    template_name = 'catalog/therapist_detail.html'
    context_object_name = 'therapist'
