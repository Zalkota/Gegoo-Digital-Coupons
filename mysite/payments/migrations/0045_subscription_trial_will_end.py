# Generated by Django 2.2.10 on 2020-04-09 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0044_subscription_invoice_upcoming'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='trial_will_end',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
