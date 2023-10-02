# Generated by Django 4.1.5 on 2023-06-15 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mailer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('title', models.CharField(max_length=500)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('body', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blogs/images/')),
                ('is_public', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_created=True, auto_now=True)),
                ('created_on', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('author', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('public', models.BooleanField(default=False)),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.blog')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, to='mainapp.tag'),
        ),
        migrations.AddField(
            model_name='blog',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.topic'),
        ),
        migrations.CreateModel(
            name='AppConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(blank=True, default='main', max_length=30, null=True, unique=True)),
                ('application_url', models.CharField(blank=True, max_length=255, null=True)),
                ('account_creation_activated', models.BooleanField(default=True)),
                ('account_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_creation_Email', to='mailer.email')),
                ('account_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_creation_email_config', to='mailer.emailconfiguration')),
                ('activate_account_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_activation_email', to='mailer.email')),
                ('activate_account_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_activation_email_config', to='mailer.emailconfiguration')),
                ('analytic_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytic_creation_email', to='mailer.email')),
                ('analytic_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytic_creation_emailconfig', to='mailer.emailconfiguration')),
                ('apply_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apply_creation_email', to='mailer.email')),
                ('apply_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apply_creation_emailconfig', to='mailer.emailconfiguration')),
                ('appointment_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointment_creation_email', to='mailer.email')),
                ('appointment_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointment_creation_emailconfig', to='mailer.emailconfiguration')),
                ('book_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_creation_email', to='mailer.email')),
                ('book_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_creation_emailconfig', to='mailer.emailconfiguration')),
                ('contact_form_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_form_email', to='mailer.email')),
                ('contact_form_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_form_emailconfig', to='mailer.emailconfiguration')),
                ('demorequest_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demorequest_creation_email', to='mailer.email')),
                ('demorequest_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demorequest_creation_emailconfig', to='mailer.emailconfiguration')),
                ('doctor_authorized_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_authorized_email', to='mailer.email')),
                ('doctor_authorized_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_authorized_emailconfig', to='mailer.emailconfiguration')),
                ('doctor_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_creation_email', to='mailer.email')),
                ('doctor_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_creation_emailconfig', to='mailer.emailconfiguration')),
                ('equip_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equip_creation_email', to='mailer.email')),
                ('equip_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equip_creation_emailconfig', to='mailer.emailconfiguration')),
                ('facility_authorized_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facility_authorized_email', to='mailer.email')),
                ('facility_authorized_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facility_authorized_emailconfig', to='mailer.emailconfiguration')),
                ('facility_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facility_creation_email', to='mailer.email')),
                ('facility_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facility_creation_emailconfig', to='mailer.emailconfiguration')),
                ('firstaid_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='firstaid_creation_email', to='mailer.email')),
                ('firstaid_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='firstaid_creation_emailconfig', to='mailer.emailconfiguration')),
                ('order_placement_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_placement_email', to='mailer.email')),
                ('order_placement_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_placement_emailconfig', to='mailer.emailconfiguration')),
                ('patient_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_creation_email', to='mailer.email')),
                ('patient_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_creation_emailconfig', to='mailer.emailconfiguration')),
                ('payment_made_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_made_email', to='mailer.email')),
                ('payment_made_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_made_emailconfig', to='mailer.emailconfiguration')),
                ('prescription_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription_creation_email', to='mailer.email')),
                ('prescription_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription_creation_emailconfig', to='mailer.emailconfiguration')),
                ('prescription_quotation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription_quotation_email', to='mailer.email')),
                ('prescription_quotation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescription_quotation_emailconfig', to='mailer.emailconfiguration')),
                ('reset_password_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='password_reset_Email', to='mailer.email')),
                ('reset_password_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='password_reset_email_config', to='mailer.emailconfiguration')),
                ('schedule_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_creation_email', to='mailer.email')),
                ('schedule_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_creation_emailconfig', to='mailer.emailconfiguration')),
                ('telehealth_creation_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telehealth_creation_email', to='mailer.email')),
                ('telehealth_creation_emailconfig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telehealth_creation_emailconfig', to='mailer.emailconfiguration')),
            ],
        ),
    ]
