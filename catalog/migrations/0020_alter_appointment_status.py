# Generated by Django 5.0.1 on 2024-02-15 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_patient_user_alter_appointment_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Pending', max_length=20),
        ),
    ]
