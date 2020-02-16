# Generated by Django 2.0.8 on 2020-01-30 03:03

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_testimonial_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, default=None, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='store-logos/'),
        ),
    ]