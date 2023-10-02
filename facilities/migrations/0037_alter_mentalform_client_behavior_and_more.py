# Generated by Django 4.1.5 on 2023-08-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0036_substanceusetitle_placeholder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentalform',
            name='client_behavior',
            field=models.ManyToManyField(blank=True, to='facilities.clientbehavior'),
        ),
        migrations.AlterField(
            model_name='mentalform',
            name='intervention_terminologies',
            field=models.ManyToManyField(blank=True, to='facilities.interventionterminology'),
        ),
    ]
