# Generated by Django 4.0.3 on 2022-06-07 22:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('serial_number', models.CharField(blank=True, max_length=250)),
                ('public_ip_address', models.CharField(blank=True, default='192.0.2.30', max_length=250, null=True)),
                ('private_ip_address', models.CharField(blank=True, default='192.0.2.30', max_length=250, null=True)),
                ('mac_address', models.CharField(blank=True, default='F4-F2-6D-F6_1F-74', max_length=250)),
                ('dns', models.CharField(blank=True, max_length=250)),
                ('wifi_ssid', models.CharField(blank=True, max_length=250)),
                ('wifi_pass', models.CharField(blank=True, max_length=250)),
                ('address_gps_location', models.CharField(blank=True, max_length=250, null=True)),
                ('firmware_version', models.CharField(blank=True, max_length=30, null=True)),
                ('commands', models.CharField(blank=True, max_length=3000, null=True)),
            ],
        ),
    ]
