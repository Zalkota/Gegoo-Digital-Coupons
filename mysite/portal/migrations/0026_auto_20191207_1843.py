# Generated by Django 2.0.8 on 2019-12-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0025_auto_20191207_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('FOOD', 'Food & Dining'), ('VEHICLES', 'Automotive & Transportation')], db_index=True, default='FOOD', max_length=20, unique=True),
        ),
    ]
