# Generated by Django 4.1.5 on 2023-05-25 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_remove_prescriptionpatient_p_code_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PrescriptionPatient',
        ),
    ]
