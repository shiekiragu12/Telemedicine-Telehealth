# Generated by Django 4.1.5 on 2023-03-04 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0044_doctor_license_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='blood_group',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='degree',
            field=models.CharField(max_length=100),
        ),
    ]
