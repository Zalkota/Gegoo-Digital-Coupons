# Generated by Django 2.0.8 on 2020-01-04 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('portal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Merchant_Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100, null=True)),
                ('apartment_address', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(max_length=100, null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
                ('merchant', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_address', to='portal.Merchant')),
            ],
            options={
                'verbose_name_plural': 'Merchant_Addresses',
            },
        ),
        migrations.DeleteModel(
            name='Shop',
        ),
    ]
