# Generated by Django 2.0.8 on 2020-01-22 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_auto_20200120_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='plan_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]