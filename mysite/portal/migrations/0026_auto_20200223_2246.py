# Generated by Django 2.2.10 on 2020-02-23 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0025_auto_20200223_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]