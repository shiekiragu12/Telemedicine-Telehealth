# Generated by Django 4.1.5 on 2023-08-23 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0030_substanceusetitle_form_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentalform',
            name='selected_slots',
            field=models.TextField(blank=True, null=True),
        ),
    ]