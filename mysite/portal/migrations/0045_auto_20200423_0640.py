# Generated by Django 2.2.10 on 2020-04-23 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0044_auto_20200402_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]