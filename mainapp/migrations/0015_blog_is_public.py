# Generated by Django 4.1.5 on 2023-03-10 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_topic_blog_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
    ]
