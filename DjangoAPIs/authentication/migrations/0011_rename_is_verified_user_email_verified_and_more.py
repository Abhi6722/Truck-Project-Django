# Generated by Django 4.1.7 on 2023-04-17 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_remove_user_is_active_user_is_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_verified',
            new_name='email_verified',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_verified',
            field=models.BooleanField(default=False),
        ),
    ]
