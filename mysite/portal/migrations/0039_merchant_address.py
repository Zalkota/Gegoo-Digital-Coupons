# Generated by Django 2.0.8 on 2019-12-23 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_auto_20191220_0025'),
        ('portal', '0038_auto_20191223_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_address', to='location.Address'),
        ),
    ]
