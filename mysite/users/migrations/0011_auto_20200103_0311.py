# Generated by Django 2.0.8 on 2020-01-03 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200103_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_consumer',
            field=models.BooleanField(default=False, verbose_name='ConsumerStatus'),
        ),
    ]
