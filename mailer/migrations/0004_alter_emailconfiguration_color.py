# Generated by Django 4.1.5 on 2023-03-07 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0003_alter_emailconfiguration_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfiguration',
            name='color',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
