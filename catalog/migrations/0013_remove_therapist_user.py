# Generated by Django 5.0.1 on 2024-02-12 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_remove_patient_therapist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='therapist',
            name='user',
        ),
    ]
