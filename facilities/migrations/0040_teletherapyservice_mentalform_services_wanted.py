# Generated by Django 4.1.5 on 2023-08-23 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0039_mentalform_application_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeletherapyService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='mentalform',
            name='services_wanted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='facilities.teletherapyservice'),
        ),
    ]
