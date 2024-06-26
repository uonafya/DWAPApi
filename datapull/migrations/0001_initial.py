# Generated by Django 5.0.4 on 2024-04-05 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='middleware_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('syncdata', models.BooleanField(default=False)),
                ('server_url', models.URLField(blank=True, default='https://khis.pmtct.uonbi.ac.ke/api/29/analytics.json&filter=ou:', null=True)),
                ('server_username', models.CharField(default='healthit', max_length=255)),
                ('server_password', models.CharField(default='rr23H3@1th1Tmtct', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Sync Settings',
            },
        ),
        migrations.CreateModel(
            name='schedule_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync_time', models.DateTimeField()),
                ('shedule_description', models.CharField(blank=True, default='Weekely  data sync', max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Schedule Settings',
            },
        ),
    ]
