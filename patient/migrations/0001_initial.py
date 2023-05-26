# Generated by Django 4.1.5 on 2023-02-23 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(blank=True, max_length=100)),
                ('patient_name', models.CharField(blank=True, max_length=100)),
                ('patient_email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('postal_code', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('city', models.TextField(blank=True)),
                ('prescription', models.ImageField(blank=True, null=True, upload_to='media/patient')),
                ('blood', models.IntegerField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
