# Generated by Django 4.1.7 on 2023-03-14 09:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number must be entered, 10 digits allowed.', regex='\\d{10}')]),
        ),
    ]
