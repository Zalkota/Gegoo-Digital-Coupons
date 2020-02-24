# Generated by Django 2.0.8 on 2020-02-19 23:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0029_auto_20200215_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
