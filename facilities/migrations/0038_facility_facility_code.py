# Generated by Django 4.1.5 on 2023-02-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0037_remove_facility_shared_encounters_prescription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='facility_code',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
