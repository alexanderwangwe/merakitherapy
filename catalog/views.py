from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic
from django.views import View
from .models import Appointment, Patient, Therapist
from django.db import models


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


@login_required
def user_appointments(request):
    # Retrieve current user's appointments
    appointments = Appointment.objects.filter(user=request.user)

    return render(request, 'catalog/user_appointments.html',
                  context={'appointments': appointments})


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


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
    # Retrieve insights for the therapist
    therapist = Therapist.objects.get(user=request.user)  # Assuming you have a user field in Therapist model
    patients = therapist.patient_set.all()  # Assuming there's a reverse relation from Therapist to Patient

    # Calculate insights
    average_age = patients.aggregate(avg_age=models.Avg('date_of_birth'))
    gender_distribution = patients.values('gender').annotate(count=models.Count('gender'))
    services_sought_after = patients.values('service').annotate(count=models.Count('service'))

    context = {
        'therapist': therapist,
        'average_age': average_age,
        'gender_distribution': gender_distribution,
        'services_sought_after': services_sought_after,
        'total_patients': patients.count(),
    }

    return render(request, 'catalog/therapist_dashboard.html', context)
