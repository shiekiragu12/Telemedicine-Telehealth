# Generated by Django 4.1.5 on 2023-07-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_alter_appointmenttime_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmenttime',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]