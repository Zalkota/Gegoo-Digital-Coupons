# Generated by Django 2.0.8 on 2019-05-21 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0049_auto_20190316_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='stripe_price',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
