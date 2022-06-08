# Generated by Django 4.0.3 on 2022-06-08 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emulator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='charger',
            name='gateway',
            field=models.CharField(blank=True, default='172.16.1.1', max_length=250),
        ),
        migrations.AddField(
            model_name='charger',
            name='port',
            field=models.CharField(blank=True, default='8000', max_length=50),
        ),
        migrations.AddField(
            model_name='charger',
            name='subnet_mask',
            field=models.CharField(blank=True, default='172.16.1.1', max_length=250),
        ),
    ]