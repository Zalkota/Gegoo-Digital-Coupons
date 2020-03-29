# Generated by Django 2.2.10 on 2020-03-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0038_auto_20200319_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='current_period_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Period Start'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='current_period_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Period End'),
        ),
    ]