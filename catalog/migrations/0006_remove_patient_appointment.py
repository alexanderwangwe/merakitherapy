# Generated by Django 5.0.1 on 2024-02-11 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_appointment_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='appointment',
        ),
    ]
