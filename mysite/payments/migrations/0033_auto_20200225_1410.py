# Generated by Django 2.0.8 on 2020-02-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0032_subscription_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='payment_status',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
