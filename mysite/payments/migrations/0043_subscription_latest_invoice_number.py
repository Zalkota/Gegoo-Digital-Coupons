# Generated by Django 2.2.10 on 2020-03-29 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0042_auto_20200329_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='latest_invoice_number',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]