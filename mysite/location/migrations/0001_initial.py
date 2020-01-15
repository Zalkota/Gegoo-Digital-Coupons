# Generated by Django 2.0.8 on 2020-01-15 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0008_city_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='store_address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100, null=True)),
                ('apartment_address', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(max_length=100, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
            ],
            options={
                'verbose_name_plural': 'store_addresses',
            },
        ),
    ]
