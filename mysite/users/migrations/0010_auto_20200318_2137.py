# Generated by Django 2.2.10 on 2020-03-18 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_merge_20200225_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='merchantprofile',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='merchantprofile',
            name='zip',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]