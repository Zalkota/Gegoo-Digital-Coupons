# Generated by Django 2.0.8 on 2019-12-23 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('portal', '0040_remove_merchant_address'),
        ('location', '0006_auto_20191220_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant_Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=100, null=True)),
                ('apartment_address', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City')),
                ('merchant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_address', to='portal.Merchant')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region')),
            ],
            options={
                'verbose_name_plural': 'Merchant_Addresses',
            },
        ),
        migrations.RemoveField(
            model_name='address',
            name='apartment_address',
        ),
        migrations.RemoveField(
            model_name='address',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip',
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
    ]