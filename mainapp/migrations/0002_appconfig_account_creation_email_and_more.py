# Generated by Django 4.1.5 on 2023-02-02 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0002_email_identifier'),
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appconfig',
            name='account_creation_email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_creation_Email', to='mailer.email'),
        ),
        migrations.AddField(
            model_name='appconfig',
            name='account_creation_emailconfig',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_creation_email_config', to='mailer.emailconfiguration'),
        ),
    ]
