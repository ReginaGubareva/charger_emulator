import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Charger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    serial_number = models.CharField(max_length=250, null=False, blank=True)
    address_gps_location = models.CharField(max_length=250, null=True, blank=True)
    firmware_version = models.CharField(max_length=30, null=True, blank=True)
    commands = models.CharField(max_length=3000, null=True, blank=True)

    wifi_ssid = models.CharField(max_length=250, null=False, blank=True)
    wifi_pass = models.CharField(max_length=250, null=False, blank=True)

    public_ip_address = models.CharField(max_length=250, null=True, blank=True, default='192.0.2.30')
    private_ip_address = models.CharField(max_length=250, null=True, blank=True, default='192.0.2.30')
    mac_address = models.CharField(max_length=250, null=False, blank=True, default='F4-F2-6D-F6_1F-74')
    port = models.CharField(max_length=50, null=False, blank=True, default='8000')
    gateway = models.CharField(max_length=250, null=False, blank=True, default='172.16.1.1')
    subnet_mask = models.CharField(max_length=250, null=False, blank=True, default='172.16.1.1')
    dns = models.CharField(max_length=250, blank=True)


