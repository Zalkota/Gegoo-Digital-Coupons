# Generated by Django 2.0.8 on 2019-02-19 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_projectpage_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectpage',
            old_name='url',
            new_name='website_url',
        ),
    ]
