# Generated by Django 4.1.7 on 2023-03-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country_code',
            field=models.CharField(default='+91', max_length=4),
        ),
    ]
