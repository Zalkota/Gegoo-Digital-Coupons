# Generated by Django 2.0.8 on 2020-01-19 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_auto_20200119_0241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='images',
        ),
        migrations.DeleteModel(
            name='About',
        ),
    ]
