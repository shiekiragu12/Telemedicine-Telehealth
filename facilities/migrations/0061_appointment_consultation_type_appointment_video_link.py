# Generated by Django 4.1.5 on 2023-05-25 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0060_alter_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='consultation_type',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='video_link',
            field=models.CharField(blank=True, max_length=455, null=True),
        ),
    ]
