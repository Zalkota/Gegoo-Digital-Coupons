# Generated by Django 2.0.8 on 2020-01-18 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20200118_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
