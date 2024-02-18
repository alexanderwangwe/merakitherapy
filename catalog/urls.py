from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from .views import update_patient, update_appointment

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),

    # Therapist CRUD
    path('therapist_registration/', views.therapist_registration, name='therapist_registration'),
    path('therapist/', views.TherapistListView.as_view(), name='therapist_list'),
    path('therapist/<int:pk>/', views.TherapistDetailView.as_view(), name='therapist_detail'),
    path('therapist/<int:pk>/', views.TherapistDetailView.as_view(), name='therapist_detail'),
    path('update_therapist/<int:therapist_id>/', views.update_therapist, name='update_therapist'),
    path('therapist_delete/<int:therapist_id>/', views.therapist_delete, name='therapist_delete'),

    # Patient CRUD
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('patient/', views.PatientListView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('update_patient/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('patient_delete/<int:patient_id>/', views.patient_delete, name='patient_delete'),

    # Appointment CRUD
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('appointment/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('update_appointment/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('delete_appointment/<int:appointment_id>/', views.appointment_delete, name='delete_appointment'),

    # Logging in and out
    path('login/', views.login_user, name='login'),
    # TODO: fix the path for the logout view
    path('logout/', views.logout_user, name='logout'),


    path('therapist_dashboard/', views.therapist_dashboard, name='therapist_dashboard'),

]
