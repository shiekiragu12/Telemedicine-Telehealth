# Generated by Django 4.1.5 on 2023-04-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_firstaid_no_of_employees_alter_firstaid_core'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('f_name', models.CharField(blank=True, max_length=30)),
                ('l_name', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=60)),
                ('facility', models.CharField(blank=True, max_length=100)),
                ('requesting_as', models.CharField(max_length=20)),
                ('date_hosipitalized', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Demo Requests',
            },
        ),
        migrations.DeleteModel(
            name='TopButton',
        ),
        migrations.AlterField(
            model_name='firstaid',
            name='f_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='firstaid',
            name='l_name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
