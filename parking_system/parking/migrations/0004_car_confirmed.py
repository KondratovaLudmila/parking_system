# Generated by Django 5.0.6 on 2024-06-07 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0003_duration_of_parking'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]