# Generated by Django 4.1.5 on 2023-02-19 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacetical', '0009_remove_product_pharmacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacy',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
