# Generated by Django 2.0.8 on 2019-12-07 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0024_auto_20191207_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('FOOD', 'Food & Dining'), ('VEHICLES', 'Automotive & Transportation')], db_index=True, default='Food', max_length=20, unique=True),
        ),
    ]