from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models import Count, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic

from .forms import PatientRegistrationForm, TherapistAppointmentForm, TherapistRegistrationForm
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



def user_appointments(request):
    # Retrieve current user's appointments
    appointments = Appointment.objects.filter(user=request.user)

    return render(request, 'catalog/user_appointments.html', context={'appointments': appointments})


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    # TODO: fix the logout view


class MyLogoutView(LoginRequiredMixin, LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class MyView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_add_appointment'
    # Or multiple of permissions:
    # permission_required = ('catalog.can_add_appointment', 'catalog.can_edit_appointment')
    # Note that 'catalog.can_add_appointment' is the permission name, not the friendly name.
    # If you want to use the friendly name, you can use the permission's codename instead:
    # permission_required = ('catalog.add_appointment', 'catalog.change_appointment')
    # The permission_required attribute can also be a callable, which should return a list or tuple of permission names.
    # permission_required = lambda request: ('catalog.can_add_appointment', 'catalog.can_edit_appointment')
    raise_exception = True
    # If True (the default), the user will be redirected to the login page if not logged in.
    # If False, the user will be denied access if not logged in.
    # If True and the user is logged in, the user will be shown a 403 Forbidden page.
    # If False and the user is logged in, the user will be shown the view but the user has no permission.
    return_403 = False

    # If True, the user will be shown a 403 Forbidden page.
    # If False (the default), the user will be shown the login page.

    # The permission_required attribute can also be a callable, which should return a list or tuple of permission names.
    # permission_required = lambda request: ('catalog.can_add_appointment', 'catalog.can_edit_appointment')

    def get(self, request):
        # <view logic>
        pass


class AppointmentListView(generic.ListView):
    model = Appointment
    template_name = 'catalog/appointment_list.html'
    context_object_name = 'appointments'
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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



def therapist_dashboard(request):
    try:
        therapist = Therapist.objects.get(user=request.user)
        patients = therapist.patient_set.all()

        # Calculate insights
        total_patients = patients.count()
        if total_patients > 0:
            average_age = patients.aggregate(avg_age=Avg('calculate_age'))
            gender_distribution = patients.values('gender').annotate(count=Count('gender'))

            # Assuming a reverse relation from Patient to Appointment
            booked_appointments = Appointment.objects.filter(therapist=therapist, status='Confirmed')
            services_sought_after = booked_appointments.values('service').annotate(count=Count('service'))

            context = {
                'therapist': therapist,
                'total_patients': total_patients,
                'average_age': average_age['avg_age'],
                'gender_distribution': gender_distribution,
                'services_sought_after': services_sought_after,
                'total_booked_appointments': booked_appointments.count(),
            }

            return render(request, 'catalog/therapist_dashboard.html', context)
        else:
            # Handle the case where the therapist has not seen any patients
            return render(request, 'catalog/no_patients_found.html')

    except Therapist.DoesNotExist:
        # Handle the case where no therapist is found for the user
        return render(request, 'catalog/no_therapist_found.html')

    except MultipleObjectsReturned:
        # Handle the case where multiple therapists are found
        # You can log an error, redirect the user, or take appropriate action
        return render(request, 'catalog/multiple_therapists_found.html')


def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Assign the current user to the patient
            patient.save()
            return redirect('patient-detail', pk=patient.pk)  # Redirect to patient detail page
    else:
        form = PatientRegistrationForm()

    return render(request, 'catalog/patient_registration.html', {'form': form})


def therapist_registration(request):
    if request.method == 'POST':
        form = TherapistRegistrationForm(request.POST)
        if form.is_valid():
            therapist = form.save(commit=False)
            therapist.user = request.user
            therapist.save()
            return redirect('therapist-detail', pk=therapist.pk)  # Redirect to therapist detail page
    else:
        form = TherapistRegistrationForm()
        return render(request, 'catalog/therapist_registration.html', {'form': form})



def create_appointment(request, therapist_id):
    therapist = get_object_or_404(Therapist, pk=therapist_id)

    if request.method == 'POST':
        form = TherapistAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.therapist = therapist
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('therapist-detail', pk=therapist_id)
    else:
        form = TherapistAppointmentForm()

    return render(request, 'catalog/create_appointment.html', {'form': form, 'therapist': therapist})