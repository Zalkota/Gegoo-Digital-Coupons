# Generated by Django 2.0.8 on 2018-11-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0013_auto_20181111_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='total',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
