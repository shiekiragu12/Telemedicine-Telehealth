# Generated by Django 4.1.5 on 2023-08-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0033_mentalform_can_be_in_any_of_cities_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentalform',
            name='language',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]