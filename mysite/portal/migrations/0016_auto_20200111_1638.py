# Generated by Django 2.0.8 on 2020-01-11 16:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_auto_20200111_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='author',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='tag',
        ),
        migrations.AlterField(
            model_name='offer',
            name='likes',
            field=models.ManyToManyField(blank=True, editable=False, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
