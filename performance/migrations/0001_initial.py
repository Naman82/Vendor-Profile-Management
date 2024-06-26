# Generated by Django 5.0.5 on 2024-05-09 05:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalVendorPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('on_time_delivery_rate', models.FloatField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('quality_rating_avg', models.FloatField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('average_response_time', models.FloatField()),
                ('fulfillment_rate', models.FloatField(validators=[django.core.validators.MaxValueValidator(100)])),
            ],
        ),
    ]
