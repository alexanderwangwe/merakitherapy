from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),  # Use as_view() for class-based view

    path('therapist/', views.TherapistListView.as_view(), name='therapist_list'),
    path('therapist/<int:pk>/', views.TherapistDetailView.as_view(), name='therapist_detail'),

    path('patient/', views.PatientListView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),

    path('appointment/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),

    path('user_appointments/', views.user_appointments, name='user_appointments'),
    path('therapist_dashboard/', views.therapist_dashboard, name='therapist_dashboard'),

    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    # registrations
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),

]
