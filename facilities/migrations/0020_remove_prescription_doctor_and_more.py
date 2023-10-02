# Generated by Django 4.1.5 on 2023-08-20 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0019_appointment_zoom_meeting_creation_response'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='patient',
        ),
        migrations.AddField(
            model_name='prescription',
            name='appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facilities.appointment'),
        ),
    ]