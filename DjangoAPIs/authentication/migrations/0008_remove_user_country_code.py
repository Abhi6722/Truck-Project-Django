# Generated by Django 4.1.7 on 2023-03-28 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_phoneotp_id_alter_phoneotp_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country_code',
        ),
    ]
