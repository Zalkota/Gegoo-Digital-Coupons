# Generated by Django 2.0.8 on 2020-02-20 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0030_auto_20200219_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.Plan'),
        ),
    ]
