# Generated by Django 2.0.8 on 2020-01-04 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200103_0311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_consumer',
            new_name='is_approved',
        ),
    ]
