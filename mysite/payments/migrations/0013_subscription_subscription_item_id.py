# Generated by Django 2.0.8 on 2020-01-25 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0012_subscription_payment_intent_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='subscription_item_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
