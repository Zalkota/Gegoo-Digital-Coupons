# Generated by Django 2.0.8 on 2019-12-14 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_address'),
        ('portal', '0032_auto_20191211_0440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='address',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
