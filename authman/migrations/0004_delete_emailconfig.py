# Generated by Django 4.1.7 on 2024-04-04 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authman', '0003_alter_myuser_managers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmailConfig',
        ),
    ]
