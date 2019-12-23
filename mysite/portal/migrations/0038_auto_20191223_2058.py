# Generated by Django 2.0.8 on 2019-12-23 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('portal', '0037_auto_20191223_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='city',
        ),
        migrations.AddField(
            model_name='merchant',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to='cities_light.City'),
        ),
    ]
