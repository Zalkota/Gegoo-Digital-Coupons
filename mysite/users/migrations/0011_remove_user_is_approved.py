# Generated by Django 2.2.10 on 2020-03-18 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200318_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_approved',
        ),
    ]