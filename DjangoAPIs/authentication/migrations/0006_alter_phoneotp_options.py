# Generated by Django 4.1.7 on 2023-03-28 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_phoneotp_options_alter_phoneotp_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phoneotp',
            options={'ordering': ['-created_at']},
        ),
    ]
