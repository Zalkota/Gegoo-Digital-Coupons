# Generated by Django 2.0.8 on 2019-01-12 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_profile_merchandise'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='images',
        ),
    ]
