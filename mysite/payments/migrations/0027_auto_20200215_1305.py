# Generated by Django 2.0.8 on 2020-02-15 13:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0026_auto_20200215_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='plan_id',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='slug',
            field=models.CharField(blank=True, editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_id',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_item_id',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_quantity',
            field=models.PositiveIntegerField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_status',
            field=models.CharField(blank=True, editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]