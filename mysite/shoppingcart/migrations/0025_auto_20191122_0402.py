# Generated by Django 2.0.8 on 2019-11-22 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0024_auto_20191122_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='background',
            field=models.CharField(choices=[('bg-primary', 'primary'), ('bg-secondary', 'secondary'), ('bg-alt', 'alt')], default='Primary', max_length=12),
        ),
    ]