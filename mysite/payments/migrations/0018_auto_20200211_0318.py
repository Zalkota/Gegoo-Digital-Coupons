# Generated by Django 2.0.8 on 2020-02-11 03:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0017_promouser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promouser',
            name='redeemd_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Redeemed At'),
        ),
    ]