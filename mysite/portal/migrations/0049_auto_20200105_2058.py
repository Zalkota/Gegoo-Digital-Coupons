# Generated by Django 2.0.8 on 2020-01-05 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0048_auto_20200105_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='facebook_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='website_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
