# Generated by Django 4.1.5 on 2023-02-02 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0002_email_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfiguration',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='emailconfiguration',
            name='host',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='emailconfiguration',
            name='password',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='emailconfiguration',
            name='port',
            field=models.CharField(default='', max_length=100),
        ),
    ]
