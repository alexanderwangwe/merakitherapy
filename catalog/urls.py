from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),

    path('therapist/', views.TherapistListView.as_view(), name='therapist_list'),
    path('therapist/<int:pk>/', views.TherapistDetailView.as_view(), name='therapist_detail'),

    path('patient/', views.PatientListView.as_view(), name='patient_list'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),

    path('appointment/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),

    # Logging in and out
    path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    # TODO: fix the path for the user_appointments view
    # path('user_appointments/', views.user_appointments, name='user_appointments'),
    path('therapist_dashboard/', views.therapist_dashboard, name='therapist_dashboard'),

    # registrations
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('therapist_registration/', views.therapist_registration, name='therapist_registration'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
]
