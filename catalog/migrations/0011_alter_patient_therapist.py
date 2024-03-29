# Generated by Django 5.0.1 on 2024-02-12 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_patient_therapist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='therapist',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.therapist'),
        ),
    ]
