# Generated by Django 2.0.8 on 2019-12-06 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0018_auto_20191206_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='offer',
            name='merchant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offer', to='portal.Merchant'),
        ),
    ]