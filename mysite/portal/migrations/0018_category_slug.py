# Generated by Django 2.0.8 on 2020-01-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_auto_20200111_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
    ]
