# Generated by Django 2.0.8 on 2020-01-25 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_auto_20200124_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='videofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
