from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PatientRegistrationForm, TherapistRegistrationForm, AppointmentForm
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


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('index')
        else:
            messages.success(request, 'Invalid username or password. Please try again.')
            return render(request, 'registration/login.html', {})
    else:
        return render(request, 'registration/login.html', {})


# TODO: fix the logout view
def logout_user(request):
    if request.method == 'POST':
        logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


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
    # Number of patients
    num_patients = Patient.objects.count()

    # Number of appointments
    num_appointments = Appointment.objects.count()

    # Gender distribution
    gender_distribution = Patient.objects.values('gender').annotate(count=Count('gender'))
    total_gender_count = sum(entry['count'] for entry in gender_distribution)

    # Calculate percentage for each gender
    for entry in gender_distribution:
        entry['percent'] = (entry['count'] / total_gender_count) * 100

    # Most chosen specialization
    most_chosen_specialization = Therapist.objects.values('specialization').annotate(
        count=Count('specialization')).order_by('-count').first()

    context = {
        'num_patients': num_patients,
        'num_appointments': num_appointments,
        'gender_distribution': gender_distribution,
        'most_chosen_specialization': most_chosen_specialization,
    }

    return render(request, 'catalog/therapist_dashboard.html', context)


def patient_registration(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user  # Assign the current user to the patient
            patient.save()
            return redirect('catalog:patient_detail', pk=patient.pk)  # Redirect to patient detail page
    else:
        form = PatientRegistrationForm()

    return render(request, 'catalog/patient_registration.html', {'form': form})


# delete and update patients
def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient-detail', patient_id=patient.pk)
    else:
        form = PatientRegistrationForm(instance=patient)

    return render(request, 'catalog/patient_registration.html', {'form': form})


def patient_delete(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    patient.delete()
    return redirect('catalog:patient_list')


def therapist_registration(request):
    if request.method == 'POST':
        form = TherapistRegistrationForm(request.POST)
        if form.is_valid():
            therapist = form.save(commit=False)
            therapist.user = request.user
            therapist.save()
            return redirect('catalog:therapist_detail', pk=therapist.pk)  # Redirect to therapist detail page
    else:
        form = TherapistRegistrationForm()

    return render(request, 'catalog/therapist_registration.html', {'form': form})


# delete and update therapists
def update_therapist(request, therapist_id):
    therapist = get_object_or_404(Therapist, pk=therapist_id)

    if request.method == 'POST':
        form = TherapistRegistrationForm(request.POST, instance=therapist)
        if form.is_valid():
            form.save()
            return redirect('therapist-detail', patient_id=therapist.pk)
    else:
        form = TherapistRegistrationForm(instance=therapist)

    return render(request, 'catalog/therapist_registration.html', {'form': form})


def therapist_delete(request, therapist_id):
    therapist = Therapist.objects.get(pk=therapist_id)
    therapist.delete()
    return redirect('catalog:therapist_list')


def create_appointment(request):
    template_name = 'create_appointment.html'

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()

            return redirect('catalog:appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm()

    return render(request, 'catalog/create_appointment.html', {'form': form})


# update and delete appointments
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment-detail', appointment_id=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'catalog/create_appointment.html', {'form': form})


def appointment_delete(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment.delete()
    return redirect('catalog:appointment_list')
