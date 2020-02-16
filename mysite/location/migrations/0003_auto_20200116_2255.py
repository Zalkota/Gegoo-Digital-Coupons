# Generated by Django 2.0.8 on 2020-01-16 22:55

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20200116_2255'),
        ('cities_light', '0008_city_timezone'),
        ('location', '0002_store_address_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='store_location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, help_text="Enter latitude of store's location.", max_digits=11, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, help_text="Enter longitude of store's location.", max_digits=11, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
                ('store', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_address', to='portal.Store')),
            ],
            options={
                'verbose_name_plural': 'store_locations',
            },
        ),
        migrations.RemoveField(
            model_name='store_address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='store_address',
            name='store',
        ),
        migrations.DeleteModel(
            name='store_address',
        ),
    ]