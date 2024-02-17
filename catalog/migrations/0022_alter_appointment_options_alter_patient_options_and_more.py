# Generated by Django 5.0.1 on 2024-02-17 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_remove_patient_user_remove_therapist_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['date', 'time', 'therapist', 'patient', 'status']},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['name'], 'permissions': [('can_add_appointment', 'Can add appointment')]},
        ),
        migrations.AlterModelOptions(
            name='therapist',
            options={'ordering': ['name', 'specialization'], 'permissions': [('can_mark_available', 'Set therapist as available'), ('can_mark_booked', 'Set therapist as booked')]},
        ),
        migrations.RemoveField(
            model_name='patient',
            name='therapist',
        ),
    ]
