# Generated by Django 4.1.5 on 2023-07-17 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0010_alter_appointment_end_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointmentduration',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='appointmenttime',
            options={'ordering': ['order']},
        ),
    ]