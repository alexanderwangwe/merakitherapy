# Generated by Django 5.0.1 on 2024-02-12 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_remove_appointment_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='service',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
