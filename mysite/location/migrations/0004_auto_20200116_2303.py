# Generated by Django 2.0.8 on 2020-01-16 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('portal', '0004_auto_20200116_2255'),
        ('location', '0003_auto_20200116_2255'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='store_location',
            new_name='StoreLocation',
        ),
    ]
