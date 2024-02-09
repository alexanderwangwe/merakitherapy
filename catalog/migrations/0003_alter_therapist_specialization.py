# Generated by Django 5.0.1 on 2024-02-09 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_appointment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='specialization',
            field=models.CharField(blank=True, choices=[('COUPLES', 'COUPLES'), ('TRAUMA', 'TRAUMA'), ('DEPRESSION', 'DEPRESSION'), ('NUTRITIONAL', 'NUTRITIONAL'), ('FAMILY', 'FAMILY'), ('BEHAVIORAL', 'ADDICTION'), ('ADDICTION', 'ADDICTION')], default='COUPLES', help_text='Select Specialization', max_length=100),
        ),
    ]