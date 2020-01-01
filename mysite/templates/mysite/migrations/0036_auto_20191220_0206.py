# Generated by Django 2.0.8 on 2019-12-20 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('portal', '0035_auto_20191220_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='city',
        ),
        migrations.AddField(
            model_name='merchant',
            name='city',
            field=models.ManyToManyField(related_name='merchant', to='cities_light.City'),
        ),
    ]
