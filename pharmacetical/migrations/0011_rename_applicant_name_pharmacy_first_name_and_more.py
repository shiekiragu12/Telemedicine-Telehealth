# Generated by Django 4.1.5 on 2023-02-19 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacetical', '0010_pharmacy_verified_product_approved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pharmacy',
            old_name='applicant_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='alternative_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='pharmacy',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
