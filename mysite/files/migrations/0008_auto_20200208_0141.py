# Generated by Django 2.0.8 on 2020-02-08 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_videofile_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videofile',
            name='title',
        ),
        migrations.AlterField(
            model_name='videofile',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]