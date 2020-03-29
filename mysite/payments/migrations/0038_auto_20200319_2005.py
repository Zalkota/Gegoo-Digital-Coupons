# Generated by Django 2.2.10 on 2020-03-19 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0037_auto_20200226_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='created_at',
            field=models.DateField(blank=True, null=True, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='current_period_end',
            field=models.DateField(blank=True, null=True, verbose_name='Period Start'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='current_period_start',
            field=models.DateField(blank=True, null=True, verbose_name='Period End'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='unix_created_at',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='unix_current_period_end',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='unix_current_period_start',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='trial_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Trial End'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='trial_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Trial Start'),
        ),
    ]