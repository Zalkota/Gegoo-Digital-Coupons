# Generated by Django 2.0.8 on 2018-10-18 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0002_auto_20181018_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='data',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='data_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Model'), (2, 'Script')], db_index=True, default=1, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='product',
            name='height_field',
            field=models.IntegerField(default=255),
        ),
        migrations.AddField(
            model_name='product',
            name='width_field',
            field=models.IntegerField(default=255),
        ),
    ]
