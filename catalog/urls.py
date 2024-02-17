from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

from .views import MyLogoutView

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),  # Use as_view() for class-based view

    path('therapist/', views.TherapistListView.as_view(), name='therapist_list'),
    path('therapist/<int:pk>/', views.TherapistDetailView.as_view(), name='therapist_detail'),

    path('patient/', views.PatientListView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),

    path('appointment/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    # TODO: fix the path for the user_appointments view
    path('user_appointments/', views.user_appointments, name='user_appointments'),
    path('therapist_dashboard/', views.therapist_dashboard, name='therapist_dashboard'),

    # registrations
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('therapist_registration/', views.therapist_registration, name='therapist_registration'),
    # TODO: fix the path for the create_appointment view
    path('therapist/<int:therapist_id>/create_appointment/', views.create_appointment, name='create_appointment'),

    path('accounts/logout/', MyLogoutView.as_view(), name='logout'),

]
