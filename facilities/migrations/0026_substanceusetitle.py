# Generated by Django 4.1.5 on 2023-08-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0025_yesno'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubstanceUseTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]