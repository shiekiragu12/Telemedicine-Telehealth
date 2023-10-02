# Generated by Django 4.1.5 on 2023-08-23 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0037_alter_mentalform_client_behavior_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentalform',
            name='counselling_experience',
        ),
        migrations.AddField(
            model_name='mentalform',
            name='counselling_experience',
            field=models.ManyToManyField(blank=True, to='facilities.counsellingexperience'),
        ),
    ]