# Generated by Django 2.0.8 on 2020-02-26 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0035_auto_20200226_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='trial_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='trial_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='unix_trial_end',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='unix_trial_start',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]