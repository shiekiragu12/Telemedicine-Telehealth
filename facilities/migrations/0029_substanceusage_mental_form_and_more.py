# Generated by Django 4.1.5 on 2023-08-23 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0028_substanceusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='substanceusage',
            name='mental_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substance_usage', to='facilities.mentalform'),
        ),
        migrations.AlterField(
            model_name='substanceusage',
            name='substance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facilities.substance'),
        ),
    ]