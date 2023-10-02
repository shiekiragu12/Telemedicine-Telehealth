# Generated by Django 4.1.5 on 2023-08-11 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0012_doctornote_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CervicalCytology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CervicalCytologySite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ExaminationRequested',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SampleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LabTestRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urgency', models.CharField(choices=[('Normal', 'Normal'), ('Urgent', 'Urgent')], max_length=10, null=True)),
                ('sample_date', models.DateField(blank=True, null=True)),
                ('sample_time', models.TimeField(blank=True, null=True)),
                ('fasting', models.BooleanField(blank=True, null=True)),
                ('sample_type', models.CharField(blank=True, max_length=100, null=True)),
                ('other_sample_type', models.CharField(blank=True, max_length=50, null=True)),
                ('drug_therapy', models.TextField(blank=True, null=True)),
                ('other_relevant_clinical_info', models.TextField(blank=True, null=True)),
                ('last_dose', models.TextField(blank=True, null=True)),
                ('last_dose_date', models.DateField(blank=True, null=True)),
                ('last_dose_time', models.TimeField(blank=True, null=True)),
                ('additional_tests', models.TextField(blank=True, null=True)),
                ('other_cervical_cytology', models.CharField(blank=True, max_length=50, null=True)),
                ('requester_signature', models.CharField(max_length=100)),
                ('cervical_cytology', models.ManyToManyField(blank=True, to='facilities.cervicalcytology')),
                ('cervical_cytology_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='facilities.cervicalcytologysite')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facilities.doctor')),
                ('examination_requested', models.ManyToManyField(blank=True, null=True, to='facilities.examinationrequested')),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='facilities.facility')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facilities.patient')),
            ],
        ),
    ]
